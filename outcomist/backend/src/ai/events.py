"""SSE event types and formatting utilities."""

import json
from enum import Enum
from typing import Any


class SSEEventType(str, Enum):
    """SSE event types for streaming."""

    MESSAGE_START = "message_start"
    MESSAGE_DELTA = "message_delta"
    MESSAGE_COMPLETE = "message_complete"
    STATUS_UPDATE = "status_update"
    ERROR = "error"


def format_sse_event(event_type: SSEEventType, data: dict[str, Any]) -> str:
    """Format data as SSE event.

    Args:
        event_type: Type of SSE event
        data: Event data dictionary

    Returns:
        SSE-formatted string with data: prefix and double newline
    """
    event_data = {"type": event_type.value, **data}
    return f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"


def format_heartbeat() -> str:
    """Format SSE heartbeat (comment to keep connection alive)."""
    return ": heartbeat\n\n"
