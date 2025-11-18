"""Message API endpoints."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from ..ai.streaming import stream_claude_response
from ..config import settings
from ..database import MessageRole
from ..database import MessageStatus
from ..database import get_db
from ..services import MessageService
from ..services import SessionService

router = APIRouter(tags=["messages"])


# Request/Response Models
class MessageCreate(BaseModel):
    """Message creation request."""

    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    """Message response."""

    id: str
    session_id: str
    role: MessageRole
    content: str
    status: MessageStatus
    created_at: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """Convert datetime objects to ISO strings."""
        if hasattr(obj, "created_at") and hasattr(obj.created_at, "isoformat"):
            obj.created_at = obj.created_at.isoformat()
        return super().model_validate(obj, **kwargs)


class MessagePairResponse(BaseModel):
    """Response containing user message and AI response."""

    user_message: MessageResponse
    ai_message: MessageResponse


# Endpoints
@router.post(
    "/api/sessions/{session_id}/messages",
    response_model=MessagePairResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    session_id: str,
    message: MessageCreate,
    stream: bool = Query(False, description="Enable SSE streaming"),
    db: AsyncSession = Depends(get_db),
):
    """Send a message and get AI response.

    Args:
        session_id: Session ID
        message: Message content
        stream: If True, return SSE stream; if False, return complete response
        db: Database session

    Returns:
        SSE stream (if stream=True) or MessagePairResponse (if stream=False)
    """
    # Verify session exists
    session = await SessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )

    # If streaming requested, return SSE response
    if stream:

        async def event_generator():
            """Generate SSE events from Claude streaming response."""
            try:
                async for event in stream_claude_response(
                    session_id=session_id,
                    user_message=message.content,
                    db=db,
                    api_key=settings.anthropic_api_key,
                ):
                    yield event
            except Exception as e:
                yield f'data: {{"type": "error", "error": "{str(e)}"}}\n\n'

        return EventSourceResponse(
            event_generator(),
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # Otherwise, use synchronous response (Phase 1 behavior)
    try:
        user_msg, ai_msg = await MessageService.send_user_message(
            db,
            session_id=session_id,
            content=message.content,
        )

        return MessagePairResponse(
            user_message=MessageResponse.model_validate(user_msg),
            ai_message=MessageResponse.model_validate(ai_msg),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}",
        )


@router.get("/api/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_session_messages(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> list[MessageResponse]:
    """Get all messages for a session."""
    # Verify session exists
    session = await SessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )

    messages = await MessageService.get_session_messages(db, session_id)
    return [MessageResponse.model_validate(m) for m in messages]
