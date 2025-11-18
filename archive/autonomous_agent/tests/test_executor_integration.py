"""
Integration tests for Executor Agent.

These tests verify end-to-end workflows:
- Multi-step plans with dependencies
- Real file I/O operations
- Error recovery scenarios
- Memory persistence
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.agents.executor import ExecutorAgent
from src.core.contracts import (
    ExecutionPlan,
    Step,
    StepStatus,
    ToolType,
)
from src.core.working_memory import WorkingMemory


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def memory(temp_dir):
    """Create working memory instance"""
    memory_dir = Path(temp_dir) / "memory"
    return WorkingMemory(task_id="integration_test", memory_dir=str(memory_dir))


@pytest.fixture
def executor(memory):
    """Create executor agent instance"""
    return ExecutorAgent(memory, max_retries=2)


def test_complete_workflow(executor, memory, temp_dir):
    """
    Test complete workflow: research → code → write file
    """
    output_file = Path(temp_dir) / "result.txt"

    steps = [
        # Step 1: Research (gather info)
        Step(
            step_id="research",
            tool=ToolType.RESEARCH,
            inputs={
                "query": "What are the benefits of async programming?",
                "depth": "shallow",
            },
            expected_output={"type": "research_result"},
        ),
        # Step 2: Generate code based on research
        Step(
            step_id="generate_code",
            tool=ToolType.CODE_EXEC,
            inputs={
                "code": """
result = "Benefits of async programming:\\n"
result += "1. Non-blocking I/O\\n"
result += "2. Better resource utilization\\n"
result += "3. Improved responsiveness\\n"
"""
            },
            expected_output={"type": "code_result"},
            dependencies=["research"],
        ),
        # Step 3: Write results to file
        Step(
            step_id="write_results",
            tool=ToolType.FILESYSTEM,
            inputs={
                "operation": "write",
                "path": str(output_file),
                "content": "Async Programming Benefits",
            },
            expected_output={"type": "file_write_result"},
            dependencies=["generate_code"],
        ),
    ]

    plan = ExecutionPlan(
        task_id="integration_test",
        steps=steps,
        success_criteria={"output_file_exists": True},
    )

    # Execute plan
    artifacts = executor.execute_plan(plan)

    # Verify all steps completed
    assert len(artifacts) == 3
    assert all(s.status == StepStatus.COMPLETED for s in steps)

    # Verify file was created
    assert output_file.exists()
    assert "Async" in output_file.read_text()

    # Verify artifacts in memory
    stored_artifacts = memory.get_artifacts()
    assert len(stored_artifacts) == 3

    # Verify provenance chain
    write_artifact = artifacts[2]
    assert "write_results" in write_artifact.provenance
    assert "generate_code" in write_artifact.provenance
    assert "research" in write_artifact.provenance


def test_dependency_aware_execution(executor, memory):
    """
    Test that executor respects step dependencies
    """
    steps = [
        Step(
            step_id="step_a",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 'A'"},
            expected_output={},
        ),
        Step(
            step_id="step_b",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 'B'"},
            expected_output={},
            dependencies=["step_a"],
        ),
        Step(
            step_id="step_c",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 'C'"},
            expected_output={},
            dependencies=["step_a", "step_b"],
        ),
    ]

    plan = ExecutionPlan(task_id="dep_test", steps=steps, success_criteria={})

    artifacts = executor.execute_plan(plan)

    # All steps completed
    assert len(artifacts) == 3

    # Verify execution order in provenance
    artifact_c = artifacts[2]
    assert len(artifact_c.provenance) > 1  # Has dependencies in chain


def test_partial_failure_recovery(executor, memory):
    """
    Test that executor can continue after retryable errors
    """
    steps = [
        Step(
            step_id="step_1",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 1 + 1"},
            expected_output={},
        ),
        # This will fail but should be retried
        Step(
            step_id="step_2_fail",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "invalid syntax !@#"},
            expected_output={},
        ),
    ]

    plan = ExecutionPlan(task_id="partial_fail_test", steps=steps, success_criteria={})

    # Execute plan - should fail on step 2
    with pytest.raises(Exception):
        executor.execute_plan(plan)

    # Verify first step completed
    status_1 = memory.get_step_status("step_1")
    assert status_1["status"] == "completed"

    # Verify second step failed after retries
    status_2 = memory.get_step_status("step_2_fail")
    assert status_2["status"] == "failed"
    assert status_2["error"] is not None


def test_artifact_retrieval(executor, memory):
    """
    Test retrieving artifacts by various filters
    """
    steps = [
        Step(
            step_id="code_step",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "result = 'code'"},
            expected_output={},
        ),
        Step(
            step_id="research_step",
            tool=ToolType.RESEARCH,
            inputs={"query": "test"},
            expected_output={},
        ),
    ]

    plan = ExecutionPlan(task_id="retrieval_test", steps=steps, success_criteria={})
    executor.execute_plan(plan)

    # Retrieve by creator
    code_artifacts = memory.get_artifacts(created_by="code_step")
    assert len(code_artifacts) == 1
    assert code_artifacts[0].content_type == "code_result"

    # Retrieve by content type
    research_artifacts = memory.get_artifacts(content_type="research_result")
    assert len(research_artifacts) == 1
    assert research_artifacts[0].created_by == "research_step"

    # Retrieve all
    all_artifacts = memory.get_artifacts()
    assert len(all_artifacts) == 2


def test_memory_persistence(temp_dir):
    """
    Test that memory persists across executor instances
    """
    memory_dir = Path(temp_dir) / "persistent_memory"
    task_id = "persistence_test"

    # First execution
    memory1 = WorkingMemory(task_id=task_id, memory_dir=str(memory_dir))
    executor1 = ExecutorAgent(memory1)

    step = Step(
        step_id="persistent_step",
        tool=ToolType.CODE_EXEC,
        inputs={"code": "result = 'persistent'"},
        expected_output={},
    )

    artifact1 = executor1.execute_step(step)

    # Second execution (new memory instance, same DB)
    memory2 = WorkingMemory(task_id=task_id, memory_dir=str(memory_dir))

    # Retrieve artifact from first execution
    retrieved = memory2.get_artifact(artifact1.artifact_id)

    assert retrieved is not None
    assert retrieved.artifact_id == artifact1.artifact_id
    assert retrieved.content == artifact1.content
