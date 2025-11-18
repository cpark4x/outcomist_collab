"""SSE streaming endpoints for real-time AI responses."""

import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from ..ai.streaming import stream_claude_response
from ..config import settings
from ..database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/sessions/{session_id}/stream")
async def stream_session(
    session_id: UUID,
    message: str = Query(..., description="User message to send"),
    db: AsyncSession = Depends(get_db),
):
    """SSE endpoint for real-time session updates.

    Args:
        session_id: ID of the session to stream
        message: User message to send to Claude
        db: Database session

    Returns:
        EventSourceResponse with SSE stream

    Raises:
        HTTPException: If session not found
    """

    async def event_generator():
        """Generate SSE events from Claude streaming response."""
        try:
            async for event in stream_claude_response(
                session_id=session_id,
                user_message=message,
                db=db,
                api_key=settings.anthropic_api_key,
            ):
                yield event

        except Exception as e:
            logger.error(f"Error in SSE stream: {e}", exc_info=True)
            # Send error event before closing
            yield f'data: {{"type": "error", "error": "{str(e)}"}}\n\n'

    return EventSourceResponse(
        event_generator(),
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
