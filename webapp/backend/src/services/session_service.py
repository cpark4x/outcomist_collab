"""Session service."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database.models import Session
from ..database.models import SessionStatus


class SessionService:
    """Service for managing sessions."""

    @staticmethod
    async def create_session(
        db: AsyncSession,
        project_id: str,
        name: str,
    ) -> Session:
        """Create a new session.

        Args:
            db: Database session
            project_id: ID of the project
            name: Session name

        Returns:
            Created session
        """
        session = Session(
            project_id=project_id,
            name=name,
            status=SessionStatus.ACTIVE,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_project_sessions(db: AsyncSession, project_id: str) -> list[Session]:
        """Get all sessions for a project.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            List of sessions for the project
        """
        result = await db.execute(
            select(Session).where(Session.project_id == project_id).order_by(Session.updated_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_session(db: AsyncSession, session_id: str) -> Session | None:
        """Get session by ID with project relationship loaded.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            Session if found, None otherwise
        """
        result = await db.execute(
            select(Session).options(selectinload(Session.project)).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()
