"""Streaming AI service using Claude Agent SDK (replacement for anthropic API)"""

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from datetime import datetime
from pathlib import Path
from uuid import UUID

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..config import get_settings
from ..database.connection import AsyncSessionLocal
from ..database.models import Message, ProjectType, Session
from ..services.file_service import FileService
from ..services.status_service import StatusService
from ..services.verify_service import GameVerificationService
from .events import SSEEventType, format_sse_event
from .prompts import get_system_prompt
from .status import WorkPhase, emit_status_event

logger = logging.getLogger(__name__)


async def stream_claude_response_sdk(
    session_id: UUID,
    user_message: str,
    db: AsyncSession,
    api_key: str,
) -> AsyncGenerator[str, None]:
    """Stream AI response using Claude Agent SDK.

    This replaces the Anthropic Messages API with the Agent SDK,
    which provides better tool integration and context management.
    """
    accumulated_content = ""
    message_id: UUID | None = None

    try:
        # Load session and project
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

        # Save user message
        user_msg = Message(
            session_id=session_id_str,
            role="user",
            content=user_message,
            created_at=datetime.utcnow(),
        )
        db.add(user_msg)
        await db.commit()

        # Yield start event
        yield format_sse_event(
            SSEEventType.MESSAGE_START,
            {"session_id": str(session_id)},
        )

        # Transition to planning
        await StatusService.set_planning(db, str(session.project_id), "Analyzing your request...")
        yield emit_status_event(WorkPhase.UNDERSTANDING, "Analyzing your request...", 0.1)

        # Setup Agent SDK options
        project_path = Path("/tmp") / f"project_{session.project_id}"
        project_path.mkdir(parents=True, exist_ok=True)

        options = ClaudeAgentOptions(
            working_directory=str(project_path),
            system_prompt=system_prompt,
            allowed_tools=["Write", "Edit", "Read"],  # File operations only
            permission_mode="acceptEdits",  # Auto-accept file operations
        )

        # Use Agent SDK client
        async with ClaudeSDKClient(options=options) as client:
            # Send query
            await client.query(user_message)

            # Transition to working
            await StatusService.set_working(db, str(session.project_id), "Creating deliverables...")
            yield emit_status_event(WorkPhase.GENERATING, "Creating deliverables...", 0.5)

            # Stream responses
            async for msg in client.receive_response():
                # Agent SDK returns message objects
                msg_type = getattr(msg, 'type', None)

                if msg_type == 'assistant':
                    # Text content from assistant
                    content = getattr(msg, 'content', '')
                    if content:
                        accumulated_content += content
                        yield format_sse_event(
                            SSEEventType.MESSAGE_DELTA,
                            {"content": content},
                        )

                elif msg_type == 'tool_use':
                    # Agent is using a tool
                    tool_name = getattr(msg, 'name', 'unknown')
                    logger.info(f"Agent using tool: {tool_name}")

                    # Extract filename if it's a file operation
                    if tool_name in ['Write', 'Edit']:
                        try:
                            # Get the file path from tool input
                            tool_input = getattr(msg, 'input', {})
                            file_path = tool_input.get('file_path', tool_input.get('path', 'unknown'))
                            filename = Path(file_path).name if file_path != 'unknown' else 'file'

                            # Show compact file creation message
                            yield format_sse_event(
                                SSEEventType.MESSAGE_DELTA,
                                {"content": f"✓ {filename}  "},
                            )
                            accumulated_content += f"✓ {filename}  "

                            # Copy file from temp to actual project location
                            # (Agent SDK writes to working_directory, we need files in our project storage)
                            temp_file_path = project_path / filename
                            if temp_file_path.exists():
                                content = temp_file_path.read_text()
                                await FileService.create_file(
                                    db=db,
                                    project_id=str(session.project_id),
                                    session_id=str(session_id),
                                    filename=filename,
                                    content=content,
                                    mime_type=_guess_mime_type(filename),
                                )
                        except Exception as e:
                            logger.error(f"Failed to save file from agent: {e}")

                elif msg_type == 'tool_result':
                    # Tool execution result
                    pass  # Agent SDK handles this internally

            # Mark message as complete
            yield format_sse_event(
                SSEEventType.MESSAGE_COMPLETE,
                {"session_id": str(session_id)},
            )

        # Save complete assistant message
        async with AsyncSessionLocal() as save_db:
            assistant_msg = Message(
                session_id=session_id_str,
                role="assistant",
                content=accumulated_content,
                created_at=datetime.utcnow(),
            )
            save_db.add(assistant_msg)
            await save_db.commit()

            # Verify game projects
            project_result = await save_db.execute(
                select(Session).where(Session.id == session_id_str).options(selectinload(Session.project))
            )
            session_with_project = project_result.scalar_one_or_none()

            if session_with_project and session_with_project.project.type == ProjectType.GAME:
                logger.info(f"🔍 Running verification for game project {session_with_project.project_id}")

                try:
                    verifier = GameVerificationService()
                    verification_result = await verifier.verify_project_game(
                        save_db, str(session_with_project.project_id)
                    )

                    logger.info(f"📊 Verification: passed={verification_result.passed}")

                    if not verification_result.passed:
                        error_summary = "\n".join(f"- {err}" for err in verification_result.errors)
                        logger.warning(f"❌ Verification FAILED: {error_summary}")

                        yield format_sse_event(
                            SSEEventType.MESSAGE_DELTA,
                            {"content": f"\n\n⚠️ Verification found issues:\n{error_summary}\n\n"}
                        )

                        await StatusService.set_working(
                            save_db, str(session_with_project.project_id), "Needs fixes"
                        )
                        await save_db.commit()
                        return
                    else:
                        logger.info(f"✅ Verification PASSED")

                except Exception as e:
                    logger.error(f"❌ Verification exception: {e}", exc_info=True)

            # Mark complete
            await StatusService.set_complete(save_db, str(session.project_id), "Ready for review")

        # Emit complete status
        yield emit_status_event(WorkPhase.COMPLETE, "Done", 1.0)

    except Exception as e:
        logger.error(f"Error in SDK streaming: {e}", exc_info=True)
        yield format_sse_event(
            SSEEventType.ERROR,
            {"error": str(e)},
        )


def _guess_mime_type(filename: str) -> str:
    """Guess MIME type from filename extension"""
    ext = Path(filename).suffix.lower()
    mime_types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.txt': 'text/plain',
        '.md': 'text/markdown',
        '.py': 'text/x-python',
    }
    return mime_types.get(ext, 'text/plain')
