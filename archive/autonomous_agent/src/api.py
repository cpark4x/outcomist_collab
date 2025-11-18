"""
FastAPI server for the Autonomous Agent system.

This module provides the REST API interface for:
- Submitting tasks for autonomous execution
- Querying task status
- Retrieving task results
- Streaming real-time progress updates (SSE)

Contract:
    POST /tasks - Submit new task
    GET /tasks/{task_id} - Get task status
    GET /tasks/{task_id}/result - Get task result
    GET /tasks/{task_id}/stream - SSE progress updates

Design Philosophy:
- Ruthless simplicity: Direct API without over-abstraction
- Background execution: Non-blocking task processing
- Clear responses: Structured JSON with helpful messages
- CORS enabled: For web UI integration
"""

import logging
import os
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .core.contracts import TaskIntent, TaskResult
from .core.orchestrator import Orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous Agent API",
    description="REST API for autonomous task execution via P→E→V workflow",
    version="0.1.0",
)

# Enable CORS for web UI integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for task tracking
# In production, use Redis or similar for distributed state
task_store: Dict[str, Dict[str, Any]] = {}

# Initialize orchestrator
# Get API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    logger.warning("ANTHROPIC_API_KEY not set - API will fail on task execution")

orchestrator = Orchestrator(
    anthropic_api_key=anthropic_api_key or "dummy-key",
    memory_dir=os.getenv("MEMORY_DIR", "./memory"),
)


# ============================================================================
# Request/Response Models
# ============================================================================


class TaskStatus(str, Enum):
    """Task execution status"""

    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskRequest(BaseModel):
    """Request to submit a new task"""

    goal: str = Field(..., description="Task goal description", min_length=1)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the task")
    constraints: Optional[Dict[str, Any]] = Field(default=None, description="Constraints and requirements")
    user_id: str = Field(default="default_user", description="User identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "goal": "Create a Python file that prints 'Hello, World!'",
                "context": {"language": "python", "filename": "hello.py"},
                "constraints": {"max_lines": 10},
                "user_id": "user_123",
            }
        }


class TaskResponse(BaseModel):
    """Response after submitting a task"""

    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(..., description="Current task status")
    message: str = Field(..., description="Human-readable message")
    submitted_at: str = Field(..., description="ISO timestamp of submission")


class TaskStatusResponse(BaseModel):
    """Response for task status query"""

    task_id: str
    status: TaskStatus
    progress: Optional[str] = Field(None, description="Progress description")
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


class TaskResultResponse(BaseModel):
    """Response containing full task result"""

    task_id: str
    success: bool
    artifacts: list = Field(..., description="Generated artifacts")
    validation: dict = Field(..., description="Verification result")
    execution_time: float = Field(..., description="Execution time in seconds")
    plan: dict = Field(..., description="Execution plan used")
    completed_at: str
    error: Optional[str] = None


# ============================================================================
# API Endpoints
# ============================================================================


@app.get("/")
async def root():
    """API health check"""
    return {
        "service": "Autonomous Agent API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "submit_task": "POST /tasks",
            "get_status": "GET /tasks/{task_id}",
            "get_result": "GET /tasks/{task_id}/result",
        },
    }


@app.post("/tasks", response_model=TaskResponse, status_code=202)
async def submit_task(request: TaskRequest, background_tasks: BackgroundTasks) -> TaskResponse:
    """
    Submit a new task for autonomous execution.

    The task will be processed asynchronously in the background.
    Use the returned task_id to query status and retrieve results.

    Args:
        request: Task submission request

    Returns:
        TaskResponse with task_id and initial status
    """
    # Create TaskIntent
    intent = TaskIntent(
        goal=request.goal,
        context=request.context or {},
        constraints=request.constraints or {},
        user_id=request.user_id,
        task_id=None,  # Will be generated
    )

    # Generate task_id (orchestrator will do this, but we need it now)
    import uuid

    task_id = str(uuid.uuid4())
    intent.task_id = task_id

    # Store task state
    task_store[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "intent": intent,
        "result": None,
        "submitted_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "completed_at": None,
        "error": None,
    }

    # Queue task for background execution
    background_tasks.add_task(_execute_task_background, task_id, intent)

    logger.info(f"Task {task_id} submitted for execution")

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Task submitted successfully. Use task_id to query status.",
        submitted_at=task_store[task_id]["submitted_at"],
    )


@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Get the current status of a task.

    Args:
        task_id: Task identifier

    Returns:
        TaskStatusResponse with current status

    Raises:
        HTTPException: If task_id not found
    """
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task_data = task_store[task_id]

    return TaskStatusResponse(
        task_id=task_id,
        status=task_data["status"],
        progress=_get_progress_description(task_data),
        started_at=task_data.get("started_at"),
        completed_at=task_data.get("completed_at"),
        error=task_data.get("error"),
    )


@app.get("/tasks/{task_id}/result", response_model=TaskResultResponse)
async def get_task_result(task_id: str) -> TaskResultResponse:
    """
    Get the final result of a completed task.

    Args:
        task_id: Task identifier

    Returns:
        TaskResultResponse with full results

    Raises:
        HTTPException: If task not found or not completed
    """
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task_data = task_store[task_id]

    if task_data["status"] not in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        raise HTTPException(
            status_code=409,
            detail=f"Task {task_id} is still {task_data['status'].value}. Wait for completion.",
        )

    result: TaskResult = task_data["result"]

    if not result:
        raise HTTPException(status_code=500, detail="Task completed but result is missing")

    # Convert result to response format
    return TaskResultResponse(
        task_id=result.task_id,
        success=result.success,
        artifacts=[_artifact_to_dict(a) for a in result.artifacts],
        validation=_validation_to_dict(result.validation),
        execution_time=result.execution_time,
        plan=_plan_to_dict(result.plan),
        completed_at=result.completed_at.isoformat(),
        error=result.error,
    )


# ============================================================================
# Background Task Execution
# ============================================================================


async def _execute_task_background(task_id: str, intent: TaskIntent):
    """
    Execute task in background and update state.

    This function is called by FastAPI's BackgroundTasks to run
    the orchestration workflow asynchronously.

    Args:
        task_id: Task identifier
        intent: Task intent to execute
    """
    logger.info(f"Starting background execution for task {task_id}")

    try:
        # Update status to planning
        task_store[task_id]["status"] = TaskStatus.PLANNING
        task_store[task_id]["started_at"] = datetime.utcnow().isoformat()

        # Execute through orchestrator
        # Note: orchestrator.execute_task is async but we need to handle it properly
        result = await orchestrator.execute_task(intent)

        # Update final status
        task_store[task_id]["status"] = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
        task_store[task_id]["result"] = result
        task_store[task_id]["completed_at"] = result.completed_at.isoformat()

        if result.error:
            task_store[task_id]["error"] = result.error

        logger.info(f"Task {task_id} completed: success={result.success}, time={result.execution_time:.2f}s")

    except Exception as e:
        error_msg = f"Task execution failed: {str(e)}"
        logger.error(f"Task {task_id} failed: {error_msg}", exc_info=True)

        task_store[task_id]["status"] = TaskStatus.FAILED
        task_store[task_id]["error"] = error_msg
        task_store[task_id]["completed_at"] = datetime.utcnow().isoformat()


# ============================================================================
# Helper Functions
# ============================================================================


def _get_progress_description(task_data: dict) -> str:
    """Generate human-readable progress description"""
    status = task_data["status"]

    if status == TaskStatus.PENDING:
        return "Task queued for execution"
    elif status == TaskStatus.PLANNING:
        return "Analyzing task and generating execution plan"
    elif status == TaskStatus.EXECUTING:
        return "Executing plan steps and generating artifacts"
    elif status == TaskStatus.VERIFYING:
        return "Verifying artifacts against success criteria"
    elif status == TaskStatus.COMPLETED:
        return "Task completed successfully"
    elif status == TaskStatus.FAILED:
        return f"Task failed: {task_data.get('error', 'Unknown error')}"
    else:
        return "Unknown status"


def _artifact_to_dict(artifact) -> dict:
    """Convert Artifact to dictionary for JSON response"""
    return {
        "artifact_id": artifact.artifact_id,
        "content": artifact.content,
        "content_type": artifact.content_type,
        "created_by": artifact.created_by,
        "metadata": artifact.metadata,
        "created_at": artifact.created_at.isoformat(),
        "provenance": artifact.provenance,
    }


def _validation_to_dict(validation) -> dict:
    """Convert ValidationResult to dictionary"""
    return {
        "passed": validation.passed,
        "confidence": validation.confidence,
        "checks": [
            {
                "check_type": c.check_type,
                "passed": c.passed,
                "details": c.details,
                "confidence": c.confidence,
            }
            for c in validation.checks
        ],
        "issues": [
            {
                "severity": i.severity,
                "description": i.description,
                "recommendation": i.recommendation,
            }
            for i in validation.issues
        ],
        "verified_at": validation.verified_at.isoformat(),
    }


def _plan_to_dict(plan) -> dict:
    """Convert ExecutionPlan to dictionary"""
    return {
        "task_id": plan.task_id,
        "steps": [
            {
                "step_id": s.step_id,
                "tool": s.tool.value,
                "status": s.status.value,
                "inputs": s.inputs,
                "expected_output": s.expected_output,
                "timeout": s.timeout,
                "dependencies": s.dependencies,
            }
            for s in plan.steps
        ],
        "success_criteria": plan.success_criteria,
        "estimated_duration": plan.estimated_duration,
        "created_at": plan.created_at.isoformat(),
    }


# ============================================================================
# Server Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
