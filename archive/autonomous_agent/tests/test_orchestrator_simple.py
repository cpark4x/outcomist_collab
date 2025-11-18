"""
Simple test to verify orchestrator can be instantiated and basic flow works.

This is a dry-run test that doesn't require API keys.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.contracts import TaskIntent
from src.core.orchestrator import Orchestrator


def test_orchestrator_initialization():
    """Test that orchestrator can be initialized"""
    print("=== Test: Orchestrator Initialization ===")

    orchestrator = Orchestrator(anthropic_api_key="test-key", memory_dir="./test_memory")

    assert orchestrator is not None
    assert orchestrator.planner is not None
    assert orchestrator.verifier is not None

    print("✓ Orchestrator initialized successfully")
    print(f"  - Planner: {orchestrator.planner.__class__.__name__}")
    print(f"  - Verifier: {orchestrator.verifier.__class__.__name__}")
    print(f"  - Memory dir: {orchestrator.memory_dir}")
    print(f"  - Max replan attempts: {orchestrator.max_replan_attempts}")


def test_task_intent_creation():
    """Test that TaskIntent can be created"""
    print("\n=== Test: TaskIntent Creation ===")

    intent = TaskIntent(goal="Test goal", context={"key": "value"}, constraints={"max_time": 60}, user_id="test_user")

    assert intent.goal == "Test goal"
    assert intent.context["key"] == "value"
    assert intent.constraints["max_time"] == 60
    assert intent.user_id == "test_user"

    print("✓ TaskIntent created successfully")
    print(f"  - Goal: {intent.goal}")
    print(f"  - Context: {intent.context}")
    print(f"  - Constraints: {intent.constraints}")


def test_api_structure():
    """Test that API module structure is correct"""
    print("\n=== Test: API Module Structure ===")

    from src.api import TaskRequest, TaskResponse, TaskStatus, app

    assert app is not None
    print("✓ FastAPI app exists")

    # Test TaskRequest model
    request = TaskRequest(goal="Test goal", context={"test": True}, user_id="test_user")
    assert request.goal == "Test goal"
    print("✓ TaskRequest model works")

    # Test TaskResponse model
    response = TaskResponse(
        task_id="test-123", status=TaskStatus.PENDING, message="Test message", submitted_at="2025-01-17T10:00:00Z"
    )
    assert response.task_id == "test-123"
    print("✓ TaskResponse model works")

    # Test available routes
    routes = [route.path for route in app.routes]
    expected_routes = ["/", "/tasks", "/tasks/{task_id}", "/tasks/{task_id}/result"]

    print("\n  Available routes:")
    for route in routes:
        print(f"    - {route}")

    for expected in expected_routes:
        assert any(expected in route for route in routes), f"Missing route: {expected}"

    print("\n✓ All expected routes present")


def run_all_tests():
    """Run all simple tests"""
    try:
        test_orchestrator_initialization()
        test_task_intent_creation()
        test_api_structure()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Running Simple Orchestrator Tests...")
    print("=" * 60)

    success = run_all_tests()
    exit(0 if success else 1)
