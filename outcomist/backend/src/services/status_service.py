"""Status management service for project status transitions and broadcasting."""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Project
from ..database.models import ProjectStatus
from .connection_manager import connection_manager

logger = logging.getLogger(__name__)


class StatusService:
    """Service for managing project status transitions and SSE broadcasting."""

    @staticmethod
    async def transition_to(
        db: AsyncSession,
        project_id: str,
        new_status: ProjectStatus,
        message: str | None = None,
        context: dict | None = None,
    ) -> Project | None:
        """Transition project to new status and broadcast update.

        Args:
            db: Database session
            project_id: Project ID to update
            new_status: New status state
            message: Optional status message (e.g., "Need clarification: X or Y?")
            context: Optional context data (agent, step, etc.)

        Returns:
            Updated project or None if not found
        """
        # Get project
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()

        if not project:
            logger.error(f"Project {project_id} not found for status transition")
            return None

        old_status = project.status

        # Update status
        project.status = new_status
        await db.commit()
        await db.refresh(project)

        logger.info(f"Project {project.name} status: {old_status} → {new_status}")

        # Note: SSE broadcasting for status updates will be added when we implement
        # project-level SSE connections. For now, status updates happen on next API call.
        # TODO: Implement broadcast_to_project in ConnectionManager

        return project

    @staticmethod
    async def get_project_status(db: AsyncSession, project_id: str) -> ProjectStatus | None:
        """Get current project status.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            Current status or None if project not found
        """
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        return project.status if project else None

    @staticmethod
    async def set_planning(
        db: AsyncSession, project_id: str, message: str = "Analyzing your request..."
    ) -> Project | None:
        """Set project status to PLANNING.

        Args:
            db: Database session
            project_id: Project ID
            message: Planning status message

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.PLANNING, message, {"agent": "planner"}
        )

    @staticmethod
    async def set_working(
        db: AsyncSession, project_id: str, message: str = "Creating deliverables..."
    ) -> Project | None:
        """Set project status to WORKING.

        Args:
            db: Database session
            project_id: Project ID
            message: Working status message

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.WORKING, message, {"agent": "executor"}
        )

    @staticmethod
    async def set_needs_input(
        db: AsyncSession, project_id: str, message: str
    ) -> Project | None:
        """Set project status to NEEDS_INPUT.

        Args:
            db: Database session
            project_id: Project ID
            message: Question or clarification needed

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.NEEDS_INPUT, message, {"agent": "planner"}
        )

    @staticmethod
    async def set_verifying(
        db: AsyncSession, project_id: str, message: str = "Checking quality..."
    ) -> Project | None:
        """Set project status to VERIFYING.

        Args:
            db: Database session
            project_id: Project ID
            message: Verification status message

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.VERIFYING, message, {"agent": "verifier"}
        )

    @staticmethod
    async def set_complete(
        db: AsyncSession, project_id: str, message: str = "Ready for review"
    ) -> Project | None:
        """Set project status to COMPLETE.

        Args:
            db: Database session
            project_id: Project ID
            message: Completion message

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.COMPLETE, message, {"agent": "verifier"}
        )

    @staticmethod
    async def set_idle(
        db: AsyncSession, project_id: str, message: str = "Waiting for task"
    ) -> Project | None:
        """Set project status to IDLE.

        Args:
            db: Database session
            project_id: Project ID
            message: Idle status message

        Returns:
            Updated project
        """
        return await StatusService.transition_to(
            db, project_id, ProjectStatus.IDLE, message, {"agent": None}
        )
