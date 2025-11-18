"""Status event types for progress indication."""

from enum import Enum

from .events import SSEEventType
from .events import format_sse_event


class WorkPhase(str, Enum):
    """Work phases for progress indication."""

    UNDERSTANDING = "understanding"
    PLANNING = "planning"
    THINKING = "thinking"
    GENERATING = "generating"
    TOOL_USE = "tool_use"
    COMPLETE = "complete"


def emit_status_event(phase: WorkPhase, message: str, progress: float) -> str:
    """Format a status update as SSE event.

    Args:
        phase: Current work phase
        message: Contextual status message
        progress: Progress from 0.0 to 1.0

    Returns:
        SSE-formatted event string
    """
    return format_sse_event(
        SSEEventType.STATUS_UPDATE,
        {
            "phase": phase.value,
            "message": message,
            "progress": progress,
        },
    )
