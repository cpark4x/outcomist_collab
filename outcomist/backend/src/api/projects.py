"""Project API endpoints."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import ProjectStatus
from ..database import ProjectType
from ..database import get_db
from ..services import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])


# Request/Response Models
class ProjectCreate(BaseModel):
    """Project creation request."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    type: ProjectType


class ProjectUpdate(BaseModel):
    """Project update request."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectResponse(BaseModel):
    """Project response."""

    id: str
    name: str
    description: str | None
    type: ProjectType
    status: ProjectStatus
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, project) -> "ProjectResponse":
        """Convert from database model."""
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            type=project.type,
            status=project.status,
            created_at=project.created_at.isoformat() + "Z",
            updated_at=project.updated_at.isoformat() + "Z",
        )


# Endpoints
@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Create a new project."""
    created_project = await ProjectService.create_project(
        db,
        name=project.name,
        description=project.description,
        project_type=project.type,
    )
    return ProjectResponse.from_model(created_project)


@router.get("", response_model=list[ProjectResponse])
async def get_all_projects(
    db: AsyncSession = Depends(get_db),
) -> list[ProjectResponse]:
    """Get all projects."""
    projects = await ProjectService.get_all_projects(db)
    return [ProjectResponse.from_model(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Get project by ID."""
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return ProjectResponse.from_model(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Update project."""
    updated_project = await ProjectService.update_project(
        db,
        project_id=project_id,
        name=update.name,
        description=update.description,
        status=update.status,
    )
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return ProjectResponse.from_model(updated_project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete project."""
    deleted = await ProjectService.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
