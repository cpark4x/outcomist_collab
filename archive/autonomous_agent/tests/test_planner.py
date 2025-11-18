"""
Tests for Planner Agent.

These tests verify that the Planner can:
1. Generate valid execution plans from task intents
2. Create plans with proper dependencies
3. Handle replanning after failures
4. Retry API calls with exponential backoff
"""

from unittest.mock import Mock, patch

import pytest

from src.agents.planner import PlannerAgent
from src.core.contracts import StepStatus, TaskIntent, ToolType


@pytest.fixture
def sample_intent():
    """Sample task intent for testing"""
    return TaskIntent(
        goal="Create a Python file that calculates fibonacci(10)",
        context={"language": "python", "function": "fibonacci"},
        constraints={"max_steps": 5},
        task_id="test_task_001",
        user_id="test_user",
    )


@pytest.fixture
def mock_claude_response():
    """Mock successful Claude API response"""
    return {
        "steps": [
            {
                "step_id": "step_1",
                "tool": "research",
                "inputs": {"query": "fibonacci algorithm implementation"},
                "expected_output": {
                    "type": "object",
                    "properties": {"algorithm": {"type": "string"}},
                },
                "timeout": 300,
                "dependencies": [],
            },
            {
                "step_id": "step_2",
                "tool": "code_exec",
                "inputs": {"code": "def fibonacci(n): ..."},
                "expected_output": {
                    "type": "object",
                    "properties": {"result": {"type": "integer"}},
                },
                "timeout": 300,
                "dependencies": ["step_1"],
            },
            {
                "step_id": "step_3",
                "tool": "filesystem",
                "inputs": {"path": "fibonacci.py", "content": "..."},
                "expected_output": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                },
                "timeout": 300,
                "dependencies": ["step_2"],
            },
        ],
        "success_criteria": {
            "primary": ["File exists", "Code runs without errors", "Output is 55"],
            "validation": ["Syntax is valid", "Function is defined"],
        },
        "estimated_duration": 900,
    }


class TestPlannerAgent:
    """Test suite for PlannerAgent"""

    def test_initialization(self):
        """Test that PlannerAgent initializes correctly"""
        planner = PlannerAgent(api_key="test_key")

        assert planner.model == "claude-3-5-sonnet-20241022"
        assert planner.max_retries == 3
        assert planner.client is not None

    @patch("src.agents.planner.Anthropic")
    def test_plan_generation(self, mock_anthropic, sample_intent, mock_claude_response):
        """Test successful plan generation"""
        # Setup mock
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text=str(mock_claude_response).replace("'", '"'))]
        mock_client.messages.create.return_value = mock_response

        # Create planner and generate plan
        planner = PlannerAgent(api_key="test_key")
        plan = planner.plan(sample_intent)

        # Verify plan structure
        assert plan.task_id == "test_task_001"
        assert len(plan.steps) == 3
        assert plan.estimated_duration == 900

        # Verify steps
        assert plan.steps[0].step_id == "step_1"
        assert plan.steps[0].tool == ToolType.RESEARCH
        assert plan.steps[0].dependencies == []

        assert plan.steps[1].step_id == "step_2"
        assert plan.steps[1].tool == ToolType.CODE_EXEC
        assert plan.steps[1].dependencies == ["step_1"]

        assert plan.steps[2].step_id == "step_3"
        assert plan.steps[2].tool == ToolType.FILESYSTEM
        assert plan.steps[2].dependencies == ["step_2"]

    @patch("src.agents.planner.Anthropic")
    def test_dependency_validation(self, mock_anthropic, sample_intent):
        """Test that invalid dependencies are caught"""
        # Setup mock with invalid dependencies
        invalid_response = {
            "steps": [
                {
                    "step_id": "step_1",
                    "tool": "research",
                    "inputs": {},
                    "expected_output": {},
                    "dependencies": ["nonexistent_step"],  # Invalid!
                }
            ],
            "success_criteria": {},
            "estimated_duration": 300,
        }

        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text=str(invalid_response).replace("'", '"'))]
        mock_client.messages.create.return_value = mock_response

        planner = PlannerAgent(api_key="test_key")

        with pytest.raises(ValueError, match="depends on non-existent step"):
            planner.plan(sample_intent)

    @patch("src.agents.planner.Anthropic")
    @patch("src.agents.planner.time.sleep")  # Mock sleep to speed up test
    def test_retry_logic(self, mock_sleep, mock_anthropic, sample_intent, mock_claude_response):
        """Test that API calls retry on failure"""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        # First two calls fail, third succeeds
        mock_client.messages.create.side_effect = [
            Exception("API error 1"),
            Exception("API error 2"),
            Mock(content=[Mock(text=str(mock_claude_response).replace("'", '"'))]),
        ]

        planner = PlannerAgent(api_key="test_key", max_retries=3)
        plan = planner.plan(sample_intent)

        # Verify it succeeded after retries
        assert plan is not None
        assert len(plan.steps) == 3

        # Verify exponential backoff
        assert mock_sleep.call_count == 2  # Called before retry 2 and 3
        mock_sleep.assert_any_call(1.0)  # First retry delay
        mock_sleep.assert_any_call(2.0)  # Second retry delay

    @patch("src.agents.planner.Anthropic")
    def test_retry_exhaustion(self, mock_anthropic, sample_intent):
        """Test that RuntimeError is raised after all retries fail"""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        # All calls fail
        mock_client.messages.create.side_effect = Exception("Persistent API error")

        planner = PlannerAgent(api_key="test_key", max_retries=3)

        with pytest.raises(RuntimeError, match="Failed to generate plan after 3 attempts"):
            planner.plan(sample_intent)

    def test_prompt_building(self, sample_intent):
        """Test that planning prompts are constructed correctly"""
        planner = PlannerAgent(api_key="test_key")
        prompt = planner._build_planning_prompt(sample_intent)

        # Verify key elements are present
        assert "Create a Python file that calculates fibonacci(10)" in prompt
        assert "language: python" in prompt
        assert "fibonacci" in prompt
        assert "max_steps: 5" in prompt
        assert "3-5 step execution plan" in prompt

    def test_ready_steps_logic(self, mock_claude_response):
        """Test that get_ready_steps correctly identifies executable steps"""

        # Create plan from mock response
        planner = PlannerAgent(api_key="test_key")
        plan = planner._parse_plan_response(mock_claude_response, "test_task")

        # Initially, only step_1 should be ready (no dependencies)
        ready = plan.get_ready_steps()
        assert len(ready) == 1
        assert ready[0].step_id == "step_1"

        # Mark step_1 as completed
        plan.steps[0].status = StepStatus.COMPLETED

        # Now step_2 should be ready
        ready = plan.get_ready_steps()
        assert len(ready) == 1
        assert ready[0].step_id == "step_2"

        # Mark step_2 as completed
        plan.steps[1].status = StepStatus.COMPLETED

        # Now step_3 should be ready
        ready = plan.get_ready_steps()
        assert len(ready) == 1
        assert ready[0].step_id == "step_3"
