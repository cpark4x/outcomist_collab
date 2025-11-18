"""
Tests for the Executor Agent.

These tests verify:
- Sequential execution of steps
- Tool dispatch and execution
- Artifact generation and storage
- Error handling and retry logic
- Status tracking
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.agents.executor import ExecutionError, ExecutorAgent
from src.core.contracts import (
    ExecutionPlan,
    Step,
    StepStatus,
    ToolType,
)
from src.core.working_memory import WorkingMemory


@pytest.fixture
def temp_memory_dir():
    """Create temporary directory for memory storage"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def memory(temp_memory_dir):
    """Create working memory instance"""
    return WorkingMemory(task_id="test_task", memory_dir=temp_memory_dir)


@pytest.fixture
def executor(memory):
    """Create executor agent instance"""
    return ExecutorAgent(memory, max_retries=2)


def test_execute_code_step(executor, memory):
    """Test executing a code execution step"""
    step = Step(
        step_id="step_1",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "result = 2 + 2"},
        expected_output={"type": "number"},
        timeout=10,
    )

    artifact = executor.execute_step(step)

    assert artifact is not None
    assert artifact.created_by == "step_1"
    assert artifact.content_type == "code_result"
    assert artifact.content["result"] == 4
    assert step.status == StepStatus.COMPLETED

    # Verify stored in memory
    stored_artifact = memory.get_artifact(artifact.artifact_id)
    assert stored_artifact is not None


def test_execute_filesystem_read(executor, memory, temp_memory_dir):
    """Test filesystem read operation"""
    # Create a test file
    test_file = Path(temp_memory_dir) / "test.txt"
    test_file.write_text("Hello, World!")

    step = Step(
        step_id="step_2",
        tool=ToolType.FILESYSTEM,
        inputs={"operation": "read", "path": str(test_file)},
        expected_output={"type": "string"},
        timeout=10,
    )

    artifact = executor.execute_step(step)

    assert artifact is not None
    assert artifact.content == "Hello, World!"
    assert artifact.content_type == "file_content"
    assert step.status == StepStatus.COMPLETED


def test_execute_filesystem_write(executor, memory, temp_memory_dir):
    """Test filesystem write operation"""
    test_file = Path(temp_memory_dir) / "output.txt"

    step = Step(
        step_id="step_3",
        tool=ToolType.FILESYSTEM,
        inputs={
            "operation": "write",
            "path": str(test_file),
            "content": "Test content",
        },
        expected_output={"type": "confirmation"},
        timeout=10,
    )

    artifact = executor.execute_step(step)

    assert artifact is not None
    assert artifact.content_type == "file_write_result"
    assert step.status == StepStatus.COMPLETED

    # Verify file was created
    assert test_file.exists()
    assert test_file.read_text() == "Test content"


def test_execute_research_step(executor, memory):
    """Test research tool execution"""
    step = Step(
        step_id="step_4",
        tool=ToolType.RESEARCH,
        inputs={"query": "Python best practices", "depth": "medium"},
        expected_output={"type": "research_result"},
        timeout=10,
    )

    artifact = executor.execute_step(step)

    assert artifact is not None
    assert artifact.content_type == "research_result"
    assert "findings" in artifact.content
    assert len(artifact.content["findings"]) > 0
    assert step.status == StepStatus.COMPLETED


def test_execute_plan_sequential(executor, memory):
    """Test executing a complete plan sequentially"""
    steps = [
        Step(
            step_id="step_1",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 1 + 1"},
            expected_output={},
        ),
        Step(
            step_id="step_2",
            tool=ToolType.RESEARCH,
            inputs={"query": "test query"},
            expected_output={},
        ),
    ]

    plan = ExecutionPlan(
        task_id="test_task",
        steps=steps,
        success_criteria={},
    )

    artifacts = executor.execute_plan(plan)

    assert len(artifacts) == 2
    assert all(a.artifact_id for a in artifacts)
    assert all(s.status == StepStatus.COMPLETED for s in steps)


def test_retry_on_failure(executor, memory):
    """Test retry logic when step fails"""
    # This will fail because code has syntax error
    step = Step(
        step_id="step_fail",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "invalid syntax here !@#"},
        expected_output={},
        timeout=10,
    )

    with pytest.raises(ExecutionError) as exc_info:
        executor.execute_step(step)

    assert "failed after" in str(exc_info.value)
    assert step.status == StepStatus.FAILED


def test_provenance_tracking(executor, memory):
    """Test that provenance chain is tracked correctly"""
    step1 = Step(
        step_id="step_1",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "result = 'first'"},
        expected_output={},
    )

    step2 = Step(
        step_id="step_2",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "result = 'second'"},
        expected_output={},
        dependencies=["step_1"],
    )

    # Execute both steps
    artifact1 = executor.execute_step(step1)
    artifact2 = executor.execute_step(step2)

    # Check provenance
    assert artifact1.provenance == ["step_1"]
    assert "step_2" in artifact2.provenance


def test_status_tracking(executor, memory):
    """Test that step status is tracked correctly"""
    step = Step(
        step_id="step_status",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "result = 'test'"},
        expected_output={},
    )

    # Initially pending
    assert step.status == StepStatus.PENDING

    # Execute
    executor.execute_step(step)

    # Should be completed
    assert step.status == StepStatus.COMPLETED

    # Check in memory
    status = memory.get_step_status("step_status")
    assert status is not None
    assert status["status"] == "completed"
