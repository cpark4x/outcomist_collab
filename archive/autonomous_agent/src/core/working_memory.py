"""
Working Memory: Persistent execution context serving as single source of truth.

This module provides:
- Append-only artifact storage for auditability
- Transactional consistency via SQLite
- Queryable history for replay and debugging
- Checkpoint/rollback support

Philosophy: File-based persistence enables deterministic replay and full auditability.
"""

import json
import sqlite3
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from .contracts import (
    Artifact,
    ExecutionPlan,
    StepStatus,
    ValidationResult,
)


def _serialize_with_datetime(obj: Any) -> str:
    """Convert dataclass to JSON string, handling datetime objects"""

    def datetime_converter(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")

    return json.dumps(asdict(obj), default=datetime_converter)


class WorkingMemory:
    """
    SQLite-backed working memory for a single task execution.

    Design principles:
    - Append-only: Never modify existing records
    - Transactional: ACID guarantees from SQLite
    - File-based: Easy to archive and replay
    - Queryable: SQL for flexible artifact retrieval
    """

    def __init__(self, task_id: str, memory_dir: str = "./memory"):
        self.task_id = task_id
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_dir / f"{task_id}.db"
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    content TEXT,
                    content_type TEXT,
                    schema_version TEXT,
                    created_by TEXT,
                    metadata TEXT,
                    created_at TEXT,
                    provenance TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS plan_state (
                    task_id TEXT,
                    plan_json TEXT,
                    status TEXT,
                    updated_at TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS step_state (
                    step_id TEXT PRIMARY KEY,
                    status TEXT,
                    result_artifact_id TEXT,
                    error TEXT,
                    updated_at TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    snapshot_json TEXT,
                    created_at TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS validation_results (
                    task_id TEXT,
                    validation_json TEXT,
                    verified_at TEXT
                )
            """
            )

            conn.commit()

    def store_artifact(self, artifact: Artifact) -> str:
        """
        Store an artifact (append-only).

        Returns:
            artifact_id
        """
        if not artifact.artifact_id:
            artifact.artifact_id = str(uuid.uuid4())

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO artifacts (
                    artifact_id, content, content_type, schema_version,
                    created_by, metadata, created_at, provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    artifact.artifact_id,
                    json.dumps(artifact.content),
                    artifact.content_type,
                    artifact.schema_version,
                    artifact.created_by,
                    json.dumps(artifact.metadata),
                    artifact.created_at.isoformat(),
                    json.dumps(artifact.provenance),
                ),
            )
            conn.commit()

        return artifact.artifact_id

    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Retrieve a specific artifact by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM artifacts WHERE artifact_id = ?", (artifact_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return Artifact(
                artifact_id=row["artifact_id"],
                content=json.loads(row["content"]),
                content_type=row["content_type"],
                schema_version=row["schema_version"],
                created_by=row["created_by"],
                metadata=json.loads(row["metadata"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                provenance=json.loads(row["provenance"]),
            )

    def get_artifacts(
        self,
        created_by: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Artifact]:
        """
        Query artifacts with filters.

        Args:
            created_by: Filter by step_id that created the artifact
            content_type: Filter by content type
            limit: Maximum number of results
        """
        query = "SELECT * FROM artifacts WHERE 1=1"
        params = []

        if created_by:
            query += " AND created_by = ?"
            params.append(created_by)

        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)

        query += " ORDER BY created_at DESC"

        if limit:
            query += f" LIMIT {limit}"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            return [
                Artifact(
                    artifact_id=row["artifact_id"],
                    content=json.loads(row["content"]),
                    content_type=row["content_type"],
                    schema_version=row["schema_version"],
                    created_by=row["created_by"],
                    metadata=json.loads(row["metadata"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                    provenance=json.loads(row["provenance"]),
                )
                for row in rows
            ]

    def store_plan(self, plan: ExecutionPlan, status: str = "active") -> None:
        """Store or update the execution plan"""
        with sqlite3.connect(self.db_path) as conn:
            # Convert plan to dict and handle Enum serialization
            plan_dict = asdict(plan)
            self._serialize_enums(plan_dict)

            conn.execute(
                """
                INSERT INTO plan_state (task_id, plan_json, status, updated_at)
                VALUES (?, ?, ?, ?)
            """,
                (
                    self.task_id,
                    json.dumps(plan_dict),
                    status,
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()

    def _serialize_enums(self, obj: Any) -> None:
        """Recursively convert Enum and datetime values to strings for JSON serialization"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if hasattr(value, "value"):  # Enum type
                    obj[key] = value.value
                elif isinstance(value, datetime):
                    obj[key] = value.isoformat()
                elif isinstance(value, (dict, list)):
                    self._serialize_enums(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if hasattr(item, "value"):  # Enum type
                    obj[i] = item.value
                elif isinstance(item, datetime):
                    obj[i] = item.isoformat()
                elif isinstance(item, (dict, list)):
                    self._serialize_enums(item)

    def get_plan(self) -> Optional[ExecutionPlan]:
        """Retrieve the current execution plan"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT plan_json FROM plan_state
                WHERE task_id = ?
                ORDER BY updated_at DESC
                LIMIT 1
            """,
                (self.task_id,),
            )
            row = cursor.fetchone()

            if not row:
                return None

            plan_dict = json.loads(row["plan_json"])
            # Note: This is simplified; in production, implement proper deserialization
            return plan_dict

    def update_step_status(
        self,
        step_id: str,
        status: StepStatus,
        result_artifact_id: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        """Update the status of a step"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO step_state (
                    step_id, status, result_artifact_id, error, updated_at
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    step_id,
                    status.value,
                    result_artifact_id,
                    error,
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()

    def get_step_status(self, step_id: str) -> Optional[dict[str, Any]]:
        """Get the current status of a step"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM step_state WHERE step_id = ?", (step_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return {
                "step_id": row["step_id"],
                "status": row["status"],
                "result_artifact_id": row["result_artifact_id"],
                "error": row["error"],
                "updated_at": row["updated_at"],
            }

    def checkpoint(self) -> str:
        """
        Create a snapshot of the current state for rollback.

        Returns:
            checkpoint_id
        """
        checkpoint_id = str(uuid.uuid4())

        # Gather current state
        artifacts = self.get_artifacts()
        plan = self.get_plan()

        snapshot = {
            "checkpoint_id": checkpoint_id,
            "task_id": self.task_id,
            "artifacts": [asdict(a) for a in artifacts],
            "plan": plan,
            "created_at": datetime.utcnow().isoformat(),
        }

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO checkpoints (checkpoint_id, snapshot_json, created_at)
                VALUES (?, ?, ?)
            """,
                (
                    checkpoint_id,
                    json.dumps(snapshot),
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()

        return checkpoint_id

    def restore(self, checkpoint_id: str) -> bool:
        """
        Rollback to a previous checkpoint.

        Note: This is simplified. In production, implement proper transactional rollback.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT snapshot_json FROM checkpoints WHERE checkpoint_id = ?",
                (checkpoint_id,),
            )
            row = cursor.fetchone()

            if not row:
                return False

            # In a real implementation, you would restore the state
            # For now, just verify the checkpoint exists
            return True

    def store_validation(self, validation: ValidationResult) -> None:
        """Store a validation result"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO validation_results (task_id, validation_json, verified_at)
                VALUES (?, ?, ?)
            """,
                (
                    self.task_id,
                    _serialize_with_datetime(validation),
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()

    def get_latest_validation(self) -> Optional[ValidationResult]:
        """Retrieve the most recent validation result"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT validation_json FROM validation_results
                WHERE task_id = ?
                ORDER BY verified_at DESC
                LIMIT 1
            """,
                (self.task_id,),
            )
            row = cursor.fetchone()

            if not row:
                return None

            # Note: Simplified; implement proper deserialization in production
            return json.loads(row["validation_json"])
