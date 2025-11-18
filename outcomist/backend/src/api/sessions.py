"""Session API endpoints."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import SessionStatus
from ..database import get_db
from ..services import ProjectService
from ..services import SessionService

router = APIRouter(tags=["sessions"])


# Request/Response Models
class SessionCreate(BaseModel):
    """Session creation request."""

    name: str = Field(..., min_length=1, max_length=255)


class SessionResponse(BaseModel):
    """Session response."""

    id: str
    project_id: str
    name: str
    status: SessionStatus
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """Convert datetime objects to ISO strings."""
        if hasattr(obj, "created_at") and hasattr(obj.created_at, "isoformat"):
            obj.created_at = obj.created_at.isoformat()
        if hasattr(obj, "updated_at") and hasattr(obj.updated_at, "isoformat"):
            obj.updated_at = obj.updated_at.isoformat()
        return super().model_validate(obj, **kwargs)


# Endpoints
@router.post(
    "/api/projects/{project_id}/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_session(
    project_id: str,
    session: SessionCreate,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """Create a new session for a project."""
    # Verify project exists
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )

    created_session = await SessionService.create_session(
        db,
        project_id=project_id,
        name=session.name,
    )
    return SessionResponse.model_validate(created_session)


@router.get("/api/projects/{project_id}/sessions", response_model=list[SessionResponse])
async def get_project_sessions(
    project_id: str,
    db: AsyncSession = Depends(get_db),
) -> list[SessionResponse]:
    """Get all sessions for a project."""
    # Verify project exists
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )

    sessions = await SessionService.get_project_sessions(db, project_id)
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """Get session by ID."""
    session = await SessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )
    return SessionResponse.model_validate(session)
