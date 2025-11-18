"""File service."""

import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database.models import File
from ..utils.image_utils import validate_and_fix_image_mime

logger = logging.getLogger(__name__)


class FileService:
    """Service for managing files."""

    @staticmethod
    def _get_project_dir(project_id: str) -> Path:
        """Get project directory path.

        Args:
            project_id: Project ID

        Returns:
            Path to project directory
        """
        return settings.data_dir / "projects" / project_id / "files"

    @staticmethod
    async def create_file(
        db: AsyncSession,
        project_id: str,
        session_id: str,
        filename: str,
        content: str | bytes,
        mime_type: str = "text/plain",
    ) -> File:
        """Create a new file with automatic MIME type validation for images.

        Args:
            db: Database session
            project_id: Project ID
            session_id: Session ID
            filename: File name
            content: File content (text or binary bytes)
            mime_type: MIME type (will be validated for images)

        Returns:
            Created file
        """
        # Create project directory if it doesn't exist
        project_dir = FileService._get_project_dir(project_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        # Prepare file path
        file_path = project_dir / filename

        # Validate content is not None
        if content is None:
            raise ValueError(f"Cannot create file {filename}: content is None")

        # Handle binary content (images)
        if isinstance(content, bytes):
            # Validate and fix image MIME type if needed
            if mime_type.startswith("image/"):
                try:
                    content, mime_type = validate_and_fix_image_mime(content, mime_type, filename)
                    logger.info(f"Validated image file {filename} with MIME type {mime_type}")
                except Exception as e:
                    logger.error(f"Failed to validate image {filename}: {e}")
                    # Continue with original content but log the error

            # Write binary file
            file_path.write_bytes(content)
            size = len(content)
        else:
            # Handle text content - ensure it's a string
            if not isinstance(content, str):
                raise ValueError(f"Cannot create file {filename}: content must be str or bytes, got {type(content)}")

            file_path.write_text(content, encoding="utf-8")
            size = len(content.encode("utf-8"))

        # Create database record
        file = File(
            project_id=project_id,
            session_id=session_id,
            name=filename,
            path=str(file_path),
            mime_type=mime_type,
            size=size,
        )
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

    @staticmethod
    async def get_project_files(db: AsyncSession, project_id: str) -> list[File]:
        """Get all files for a project.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            List of files
        """
        result = await db.execute(select(File).where(File.project_id == project_id).order_by(File.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_file(db: AsyncSession, file_id: str) -> File | None:
        """Get file by ID.

        Args:
            db: Database session
            file_id: File ID

        Returns:
            File if found, None otherwise
        """
        result = await db.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_file_content(db: AsyncSession, file_id: str) -> str | None:
        """Get file content.

        Args:
            db: Database session
            file_id: File ID

        Returns:
            File content if found, None otherwise
        """
        file = await FileService.get_file(db, file_id)
        if not file:
            return None

        try:
            return Path(file.path).read_text(encoding="utf-8")
        except Exception:
            return None

    @staticmethod
    async def delete_file(db: AsyncSession, file_id: str) -> bool:
        """Delete file.

        Args:
            db: Database session
            file_id: File ID

        Returns:
            True if deleted, False if not found
        """
        file = await FileService.get_file(db, file_id)
        if not file:
            return False

        # Delete file from disk
        try:
            Path(file.path).unlink(missing_ok=True)
        except Exception:
            pass

        # Delete database record
        await db.delete(file)
        await db.commit()
        return True
