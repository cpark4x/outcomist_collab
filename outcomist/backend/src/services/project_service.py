"""Project service."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Project
from ..database.models import ProjectStatus
from ..database.models import ProjectType


class ProjectService:
    """Service for managing projects."""

    @staticmethod
    async def create_project(
        db: AsyncSession,
        name: str,
        description: str | None,
        project_type: ProjectType,
    ) -> Project:
        """Create a new project.

        Args:
            db: Database session
            name: Project name
            description: Project description
            project_type: Type of project

        Returns:
            Created project
        """
        project = Project(
            name=name,
            description=description,
            type=project_type,
            status=ProjectStatus.ACTIVE,
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def get_all_projects(db: AsyncSession) -> list[Project]:
        """Get all projects.

        Args:
            db: Database session

        Returns:
            List of all projects
        """
        result = await db.execute(select(Project).order_by(Project.updated_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_project(db: AsyncSession, project_id: str) -> Project | None:
        """Get project by ID.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            Project if found, None otherwise
        """
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_project(
        db: AsyncSession,
        project_id: str,
        name: str | None = None,
        description: str | None = None,
        status: ProjectStatus | None = None,
    ) -> Project | None:
        """Update project.

        Args:
            db: Database session
            project_id: Project ID
            name: New name (optional)
            description: New description (optional)
            status: New status (optional)

        Returns:
            Updated project if found, None otherwise
        """
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return None

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status

        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: str) -> bool:
        """Delete project.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            True if deleted, False if not found
        """
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return False

        await db.delete(project)
        await db.commit()
        return True
