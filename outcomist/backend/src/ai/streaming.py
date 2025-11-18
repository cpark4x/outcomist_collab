"""Streaming AI service for real-time Claude responses."""

import asyncio
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
from ..database.models import Session
from ..services.file_service import FileService
from .events import SSEEventType
from .events import format_sse_event
from .prompts import get_system_prompt
from .tools import TOOLS

logger = logging.getLogger(__name__)


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
        result = await db.execute(
            select(Session).where(Session.id == session_id).options(selectinload(Session.project))
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
        result = await db.execute(select(Message).where(Message.session_id == session_id).order_by(Message.created_at))
        history = result.scalars().all()

        # Build messages array for Claude
        messages = []
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Save user message to database
        user_msg = Message(
            session_id=session_id,
            role="user",
            content=user_message,
            created_at=datetime.utcnow(),
        )
        db.add(user_msg)
        await db.commit()

        # Yield message start event
        yield format_sse_event(
            SSEEventType.MESSAGE_START,
            {"session_id": str(session_id)},
        )

        # Stream from Claude with tool support
        client = AsyncAnthropic(api_key=api_key)
        settings = get_settings()

        # Allow multiple tool use rounds
        max_tool_rounds = 5
        tool_round = 0

        while tool_round < max_tool_rounds:
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

            # Check if Claude used any tools
            tool_used = False
            for block in final_message.content:
                if block.type == "tool_use":
                    tool_used = True
                    tool_name = block.name
                    tool_input = block.input

                    # Handle create_file tool
                    if tool_name == "create_file":
                        filename = tool_input.get("filename")
                        content = tool_input.get("content")
                        mime_type = tool_input.get("mime_type", "text/plain")

                        # Create the file
                        await FileService.create_file(
                            db=db,
                            project_id=str(session.project_id),
                            session_id=str(session_id),
                            filename=filename,
                            content=content,
                            mime_type=mime_type,
                        )

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
                        new_name = tool_input.get("name")

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
                session_id=session_id,
                role="assistant",
                content=accumulated_content,
                created_at=datetime.utcnow(),
            )
            save_db.add(assistant_msg)
            await save_db.commit()
            await save_db.refresh(assistant_msg)
            message_id = assistant_msg.id

        # Yield completion event
        yield format_sse_event(
            SSEEventType.MESSAGE_COMPLETE,
            {
                "message_id": str(message_id),
                "content": accumulated_content,
            },
        )

    except Exception as e:
        logger.error(f"Error streaming Claude response: {e}", exc_info=True)
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
