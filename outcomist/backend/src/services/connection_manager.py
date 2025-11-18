"""Connection manager for tracking active SSE connections."""

import asyncio
import logging
from collections import defaultdict
from uuid import UUID

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage active SSE connections for real-time updates."""

    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: dict[UUID, list[asyncio.Queue]] = defaultdict(list)

    async def connect(self, session_id: UUID) -> asyncio.Queue:
        """Register new SSE connection for a session.

        Args:
            session_id: Session ID to connect to

        Returns:
            Queue for receiving events
        """
        queue: asyncio.Queue = asyncio.Queue()
        self.active_connections[session_id].append(queue)
        logger.info(f"New connection for session {session_id}. Total: {len(self.active_connections[session_id])}")
        return queue

    async def disconnect(self, session_id: UUID, queue: asyncio.Queue):
        """Remove SSE connection.

        Args:
            session_id: Session ID to disconnect from
            queue: Queue to remove
        """
        if session_id in self.active_connections:
            try:
                self.active_connections[session_id].remove(queue)
                logger.info(
                    f"Connection closed for session {session_id}. Remaining: {len(self.active_connections[session_id])}"
                )

                # Clean up empty session entries
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]
            except ValueError:
                # Queue already removed
                pass

    async def broadcast(self, session_id: UUID, event: dict):
        """Send event to all connections for a session.

        Args:
            session_id: Session ID to broadcast to
            event: Event data to send
        """
        if session_id not in self.active_connections:
            logger.debug(f"No active connections for session {session_id}")
            return

        connections = self.active_connections[session_id]
        logger.debug(f"Broadcasting to {len(connections)} connections for session {session_id}")

        # Send to all connections
        for queue in connections:
            try:
                await queue.put(event)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")

    def get_connection_count(self, session_id: UUID) -> int:
        """Get number of active connections for a session.

        Args:
            session_id: Session ID to check

        Returns:
            Number of active connections
        """
        return len(self.active_connections.get(session_id, []))

    def get_total_connections(self) -> int:
        """Get total number of active connections across all sessions.

        Returns:
            Total number of connections
        """
        return sum(len(queues) for queues in self.active_connections.values())


# Global connection manager instance
connection_manager = ConnectionManager()
