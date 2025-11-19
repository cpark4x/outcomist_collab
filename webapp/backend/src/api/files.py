"""File API endpoints."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import get_db
from ..services.file_service import FileService

router = APIRouter(prefix="/api", tags=["files"])


@router.get("/projects/{project_id}/files")
async def get_project_files(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all files for a project.

    Args:
        project_id: Project ID
        db: Database session

    Returns:
        List of files
    """
    files = await FileService.get_project_files(db, project_id)
    return [
        {
            "id": str(file.id),
            "project_id": str(file.project_id),
            "session_id": str(file.session_id) if file.session_id else None,
            "name": file.name,
            "mime_type": file.mime_type,
            "size": file.size,
            "created_at": file.created_at.isoformat(),
        }
        for file in files
    ]


@router.get("/files/{file_id}")
async def get_file(
    file_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get file by ID.

    Args:
        file_id: File ID
        db: Database session

    Returns:
        File details
    """
    file = await FileService.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "id": str(file.id),
        "project_id": str(file.project_id),
        "session_id": str(file.session_id) if file.session_id else None,
        "name": file.name,
        "mime_type": file.mime_type,
        "size": file.size,
        "created_at": file.created_at.isoformat(),
    }


@router.get("/files/{file_id}/content")
async def get_file_content(
    file_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get file content.

    Args:
        file_id: File ID
        db: Database session

    Returns:
        File content as text
    """
    content = await FileService.get_file_content(db, file_id)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found or cannot be read")

    return {"content": content}


@router.get("/files/{file_id}/download")
async def download_file(
    file_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Download file.

    Args:
        file_id: File ID
        db: Database session

    Returns:
        File as download
    """
    file = await FileService.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file.path,
        filename=file.name,
        media_type=file.mime_type,
    )


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete file.

    Args:
        file_id: File ID
        db: Database session

    Returns:
        Success message
    """
    success = await FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")

    return {"message": "File deleted successfully"}
