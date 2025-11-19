"""Message service."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..ai.agent import agent
from ..database.models import Message
from ..database.models import MessageRole
from ..database.models import MessageStatus
from .session_service import SessionService


class MessageService:
    """Service for managing messages."""

    @staticmethod
    async def create_message(
        db: AsyncSession,
        session_id: str,
        role: MessageRole,
        content: str,
        status: MessageStatus = MessageStatus.SENT,
    ) -> Message:
        """Create a new message.

        Args:
            db: Database session
            session_id: Session ID
            role: Message role
            content: Message content
            status: Message status

        Returns:
            Created message
        """
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            status=status,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def get_session_messages(db: AsyncSession, session_id: str) -> list[Message]:
        """Get all messages for a session.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            List of messages in chronological order
        """
        result = await db.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def send_user_message(
        db: AsyncSession,
        session_id: str,
        content: str,
    ) -> tuple[Message, Message]:
        """Send user message and get AI response.

        Args:
            db: Database session
            session_id: Session ID
            content: User message content

        Returns:
            Tuple of (user_message, ai_message)

        Raises:
            ValueError: If session not found
        """
        # Get session with project
        session = await SessionService.get_session(db, session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Create user message
        user_message = await MessageService.create_message(
            db,
            session_id=session_id,
            role=MessageRole.USER,
            content=content,
        )

        # Get conversation history
        conversation_history = await MessageService.get_session_messages(db, session_id)

        try:
            # Get AI response
            ai_response = agent.send_message(
                project=session.project,
                conversation_history=conversation_history,
                user_message=content,
            )

            # Create AI message
            ai_message = await MessageService.create_message(
                db,
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=ai_response,
                status=MessageStatus.SENT,
            )

            return user_message, ai_message

        except Exception as e:
            # Create failed AI message
            ai_message = await MessageService.create_message(
                db,
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=f"Error: {str(e)}",
                status=MessageStatus.FAILED,
            )
            raise
