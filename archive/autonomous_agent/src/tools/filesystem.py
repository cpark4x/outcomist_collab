"""
Filesystem Tool: Read and write files.

MVP Implementation:
- Direct file system access
- Basic path validation
- No sandboxing

Future V1.0:
- Sandboxed file system access
- Path restrictions
- Size limits
- File type validation
"""

import logging
from pathlib import Path
from typing import Any, Dict

from ..core.working_memory import WorkingMemory

logger = logging.getLogger(__name__)


def execute(inputs: Dict[str, Any], memory: WorkingMemory) -> Dict[str, Any]:
    """
    Execute filesystem operations.

    Args:
        inputs: Dictionary containing:
            - operation: "read" or "write"
            - path: File path
            - content: Content to write (for write operation)
        memory: Working memory for artifact access

    Returns:
        Dictionary containing:
            - content: File content (for read) or confirmation (for write)
            - content_type: "file_content" or "file_write_result"
            - success: Boolean indicating success
            - error: Error message if operation failed
    """
    operation = inputs.get("operation", "")
    file_path = inputs.get("path", "")

    if not operation or not file_path:
        return {
            "content": "",
            "content_type": "error",
            "error": "Missing operation or path",
            "success": False,
        }

    path = Path(file_path)

    try:
        if operation == "read":
            return _read_file(path)
        elif operation == "write":
            content = inputs.get("content", "")
            return _write_file(path, content)
        else:
            return {
                "content": "",
                "content_type": "error",
                "error": f"Unknown operation: {operation}",
                "success": False,
            }

    except Exception as e:
        error_msg = f"Filesystem operation failed: {str(e)}"
        logger.error(error_msg)
        return {
            "content": "",
            "content_type": "error",
            "error": error_msg,
            "success": False,
        }


def _read_file(path: Path) -> Dict[str, Any]:
    """Read file content"""
    logger.info(f"Reading file: {path}")

    if not path.exists():
        return {
            "content": "",
            "content_type": "file_content",
            "error": f"File not found: {path}",
            "success": False,
        }

    content = path.read_text()
    logger.info(f"Read {len(content)} characters from {path}")

    return {
        "content": content,
        "content_type": "file_content",
        "path": str(path),
        "size": len(content),
        "success": True,
    }


def _write_file(path: Path, content: str) -> Dict[str, Any]:
    """Write content to file"""
    logger.info(f"Writing to file: {path}")

    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write content
    path.write_text(content)
    logger.info(f"Wrote {len(content)} characters to {path}")

    return {
        "content": f"Successfully wrote {len(content)} characters to {path}",
        "content_type": "file_write_result",
        "path": str(path),
        "size": len(content),
        "success": True,
    }
