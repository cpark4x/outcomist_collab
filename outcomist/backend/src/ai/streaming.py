"""Streaming AI service for real-time Claude responses."""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from datetime import datetime
from uuid import UUID

from anthropic import AsyncAnthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..config import get_settings
from ..database.connection import AsyncSessionLocal
from ..database.models import Message
from ..database.models import ProjectStatus
from ..database.models import ProjectType
from ..database.models import Session
from ..services.file_service import FileService
from ..services.status_service import StatusService
from ..services.verify_service import GameVerificationService
from ..utils.image_utils import validate_base64_image
from .events import SSEEventType
from .events import format_sse_event
from .prompts import get_system_prompt
from .status import WorkPhase
from .status import emit_status_event
from .tools import TOOLS

logger = logging.getLogger(__name__)


async def _validate_message_content(content: str | list | dict) -> str | list | dict | None:
    """Validate and fix message content, especially images with MIME type issues.

    Args:
        content: Message content (string, list of content blocks, or dict)

    Returns:
        Validated content, or None if content is completely invalid
    """
    # If content is a simple string, try to parse as JSON first
    if isinstance(content, str):
        # Try to parse as JSON in case it's serialized structured content
        try:
            parsed = json.loads(content)
            if isinstance(parsed, (list, dict)):
                # It was JSON-serialized structured content
                logger.debug(f"Parsed JSON-serialized content: {type(parsed)}")
                content = parsed
            else:
                # It was a JSON string value, return as-is
                return content
        except (json.JSONDecodeError, TypeError):
            # Not JSON, return as-is
            return content

    # If content is a dict, check if it's a single content block
    if isinstance(content, dict):
        content = [content]

    # If content is a list, validate each block
    if isinstance(content, list):
        validated_blocks = []

        for block in content:
            # Handle text blocks
            if isinstance(block, str):
                validated_blocks.append(block)
                continue

            if not isinstance(block, dict):
                continue

            block_type = block.get("type")

            # Handle image blocks with validation
            if block_type == "image":
                source = block.get("source", {})
                if source.get("type") == "base64":
                    b64_data = source.get("data")
                    media_type = source.get("media_type", "image/jpeg")

                    # Validate and fix the image
                    result = validate_base64_image(b64_data, media_type)

                    if result is not None:
                        fixed_b64, correct_mime = result
                        # Update the block with fixed data
                        validated_block = {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": correct_mime,
                                "data": fixed_b64,
                            },
                        }
                        validated_blocks.append(validated_block)
                        logger.info(f"Validated and fixed image block: {media_type} -> {correct_mime}")
                    else:
                        # Skip invalid images
                        logger.warning(f"Skipping invalid image block with MIME type {media_type}")
                        continue
                else:
                    # Non-base64 image source, keep as-is
                    validated_blocks.append(block)
            else:
                # Other block types (text, tool_use, tool_result, etc.)
                validated_blocks.append(block)

        # Return validated blocks, or None if all blocks were invalid
        return validated_blocks if validated_blocks else None

    # Fallback: return original content
    return content


async def stream_claude_response(
    session_id: UUID,
    user_message: str,
    db: AsyncSession,
    api_key: str,
) -> AsyncGenerator[str, None]:
    """Stream AI response using Claude's streaming API.

    Yields SSE-formatted events:
    - message_start: When streaming begins
    - message_delta: Content chunks as they arrive
    - message_complete: When streaming finishes (with complete message)
    - error: If any error occurs

    Args:
        session_id: ID of the session
        user_message: User's message text
        db: Database session
        api_key: Anthropic API key

    Yields:
        SSE-formatted event strings
    """
    accumulated_content = ""
    message_id: UUID | None = None

    try:
        # Load session and project (eagerly load project to avoid lazy-loading error)
        # Convert UUID to string for query since Session.id is String type
        session_id_str = str(session_id)
        result = await db.execute(
            select(Session).where(Session.id == session_id_str).options(selectinload(Session.project))
        )
        session = result.scalar_one_or_none()

        if not session:
            yield format_sse_event(
                SSEEventType.ERROR,
                {"error": f"Session {session_id} not found"},
            )
            return

        # Get system prompt
        system_prompt = get_system_prompt(session.project.type)

        # Load conversation history
        result = await db.execute(select(Message).where(Message.session_id == session_id_str).order_by(Message.created_at))
        history = result.scalars().all()

        # Build messages array for Claude with image validation
        messages = []
        for idx, msg in enumerate(history):
            logger.debug(f"Processing history message {idx}: role={msg.role}, content_type={type(msg.content)}")
            content = await _validate_message_content(msg.content)
            if content is not None:  # Skip messages with invalid content
                messages.append({"role": msg.role, "content": content})
            else:
                logger.warning(f"Skipped invalid message {idx} from history")

        # Add current user message (also validate if it contains images)
        logger.debug(f"Processing user message: type={type(user_message)}, preview={str(user_message)[:100]}")
        validated_user_message = await _validate_message_content(user_message)
        messages.append({"role": "user", "content": validated_user_message})

        logger.info(f"Built {len(messages)} messages for Claude API (history: {len(history)}, current: 1)")

        # Save user message to database
        user_msg = Message(
            session_id=session_id_str,
            role="user",
            content=user_message,
            created_at=datetime.utcnow(),
        )
        db.add(user_msg)
        await db.commit()

        # Yield message start event (MUST yield first to start generator iteration)
        yield format_sse_event(
            SSEEventType.MESSAGE_START,
            {"session_id": str(session_id)},
        )

        # Transition to PLANNING status (after first yield so generator executes)
        await StatusService.set_planning(db, str(session.project_id), "Analyzing your request...")

        # Emit understanding status
        yield emit_status_event(
            WorkPhase.UNDERSTANDING,
            "Analyzing your request...",
            0.1,
        )

        # Stream from Claude with tool support
        client = AsyncAnthropic(api_key=api_key)
        settings = get_settings()

        # Allow multiple tool use rounds
        max_tool_rounds = 5
        tool_round = 0

        while tool_round < max_tool_rounds:
            # Emit generating status before streaming
            if tool_round == 0:
                # Transition to WORKING status
                await StatusService.set_working(db, str(session.project_id), "Crafting response...")

                yield emit_status_event(
                    WorkPhase.GENERATING,
                    "Crafting response...",
                    0.5,
                )

            try:
                async with client.messages.stream(
                    model=settings.claude_model,
                    max_tokens=settings.claude_max_tokens,
                    system=system_prompt,
                    messages=messages,
                    tools=TOOLS,
                ) as stream:
                    async for text in stream.text_stream:
                        accumulated_content += text
                        yield format_sse_event(
                            SSEEventType.MESSAGE_DELTA,
                            {"content": text},
                        )

                    # Get final message to check for tool use
                    final_message = await stream.get_final_message()

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Claude API error: {error_msg}")

                # If it's an image MIME type error, log the messages being sent
                if "Image does not match" in error_msg or "media type" in error_msg:
                    logger.error(f"Image MIME type error detected. Total messages: {len(messages)}")
                    for idx, msg in enumerate(messages):
                        msg_content = msg.get("content", "")
                        if isinstance(msg_content, list):
                            for block_idx, block in enumerate(msg_content):
                                if isinstance(block, dict) and block.get("type") == "image":
                                    source = block.get("source", {})
                                    media_type = source.get("media_type", "unknown")
                                    logger.error(
                                        f"Message {idx}, block {block_idx}: image with media_type={media_type}"
                                    )

                # Re-raise the error
                raise

            # Check if Claude used any tools
            tool_used = False
            for block in final_message.content:
                if block.type == "tool_use":
                    tool_used = True
                    tool_name = block.name
                    tool_input = block.input

                    # Handle create_file tool
                    if tool_name == "create_file":
                        filename = tool_input.get("filename", "file")

                        # Emit tool use status
                        yield emit_status_event(
                            WorkPhase.TOOL_USE,
                            f"Creating {filename}...",
                            0.7,
                        )
                        content = tool_input.get("content")
                        mime_type = tool_input.get("mime_type", "text/plain")

                        # Only create file if content is provided and not None/empty
                        if content is not None and content != "":
                            try:
                                await FileService.create_file(
                                    db=db,
                                    project_id=str(session.project_id),
                                    session_id=str(session_id),
                                    filename=filename,
                                    content=content,
                                    mime_type=mime_type,
                                )
                            except ValueError as e:
                                logger.error(f"Failed to create file {filename}: {e}")
                                # Continue without crashing - just log the error
                        else:
                            logger.warning(f"Skipping file creation for {filename}: content is None or empty")

                        # Send file creation event
                        yield format_sse_event(
                            SSEEventType.MESSAGE_DELTA,
                            {"content": f"\n\n[Created file: {filename}]\n\n"},
                        )
                        accumulated_content += f"\n\n[Created file: {filename}]\n\n"

                        # Add tool result to conversation
                        messages.append(
                            {
                                "role": "assistant",
                                "content": final_message.content,
                            }
                        )
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": block.id,
                                        "content": f"File '{filename}' created successfully",
                                    }
                                ],
                            }
                        )

                    # Handle update_project_name tool
                    elif tool_name == "update_project_name":
                        new_name = tool_input.get("name", "project")

                        # Emit tool use status
                        yield emit_status_event(
                            WorkPhase.TOOL_USE,
                            f"Updating project name to '{new_name}'...",
                            0.7,
                        )

                        # Update project name in database
                        session.project.name = new_name
                        await db.commit()

                        # Add tool result to conversation
                        messages.append(
                            {
                                "role": "assistant",
                                "content": final_message.content,
                            }
                        )
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": block.id,
                                        "content": f"Project renamed to '{new_name}'",
                                    }
                                ],
                            }
                        )

            # If no tool was used, we're done
            if not tool_used:
                break

            tool_round += 1

        # Save complete assistant message to database using a fresh session
        # (the original db session may be closed by FastAPI after returning EventSourceResponse)
        async with AsyncSessionLocal() as save_db:
            assistant_msg = Message(
                session_id=session_id_str,
                role="assistant",
                content=accumulated_content,
                created_at=datetime.utcnow(),
            )
            save_db.add(assistant_msg)
            await save_db.commit()
            await save_db.refresh(assistant_msg)
            message_id = assistant_msg.id

            # Get project to check type (CAREFUL: use fresh query in this session)
            project_result = await save_db.execute(
                select(Session).where(Session.id == session_id_str).options(selectinload(Session.project))
            )
            session_with_project = project_result.scalar_one_or_none()

            # Verify game projects before marking complete
            if session_with_project and session_with_project.project.type == ProjectType.GAME:
                logger.info(f"🔍 Running verification for game project {session_with_project.project_id}")

                # Run verification
                verifier = GameVerificationService()
                verification_result = await verifier.verify_project_game(save_db, str(session_with_project.project_id))

                if not verification_result.passed:
                    # Verification failed - log and report
                    error_summary = "\n".join(f"- {err}" for err in verification_result.errors)
                    logger.warning(f"❌ Verification FAILED: {error_summary}")

                    # Add verification failure to stream
                    yield format_sse_event(
                        SSEEventType.MESSAGE_DELTA,
                        {"content": f"\n\n⚠️ Verification found issues:\n{error_summary}\n\n"}
                    )

                    # Don't mark complete - stay in working status
                    await StatusService.set_working(save_db, str(session_with_project.project_id), "Needs fixes")
                    await save_db.commit()
                    return
                else:
                    logger.info(f"✅ Verification PASSED")

            # Transition to COMPLETE status (only if verification passed or not a game)
            await StatusService.set_complete(save_db, str(session.project_id), "Ready for review")

        # Emit complete status
        yield emit_status_event(
            WorkPhase.COMPLETE,
            "Done",
            1.0,
        )

        # Yield completion event
        yield format_sse_event(
            SSEEventType.MESSAGE_COMPLETE,
            {
                "message_id": str(message_id),
                "content": accumulated_content,
            },
        )

    except Exception as e:
        logger.error(f"❌ EXCEPTION in stream_claude_response: {e}", exc_info=True)
        yield format_sse_event(
            SSEEventType.ERROR,
            {"error": str(e)},
        )


async def heartbeat_generator(interval: int = 15) -> AsyncGenerator[str, None]:
    """Generate periodic heartbeat comments to keep SSE connection alive.

    Args:
        interval: Seconds between heartbeats

    Yields:
        SSE heartbeat comments
    """
    while True:
        await asyncio.sleep(interval)
        yield ": heartbeat\n\n"
