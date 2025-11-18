"""
Integration test for the full API workflow.

This script tests the complete P→E→V flow through the API:
1. Start the server (manually or via subprocess)
2. Submit a simple task
3. Poll for status
4. Retrieve and validate the result
"""

import time
from typing import Any, Dict

import requests

# API Configuration
API_BASE_URL = "http://localhost:8000"
POLL_INTERVAL = 2  # seconds
MAX_WAIT_TIME = 60  # seconds


def test_api_health():
    """Test that the API is running and healthy"""
    print("=== Testing API Health ===")
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200, f"API health check failed: {response.status_code}"

    data = response.json()
    print(f"✓ API is running: {data['service']} v{data['version']}")
    print(f"  Status: {data['status']}")
    return True


def submit_task(goal: str, context: Dict[str, Any] = None) -> str:
    """Submit a task and return task_id"""
    print("\n=== Submitting Task ===")
    print(f"Goal: {goal}")

    payload = {"goal": goal, "context": context or {}, "user_id": "test_user"}

    response = requests.post(f"{API_BASE_URL}/tasks", json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 202, f"Task submission failed: {response.status_code}"

    data = response.json()
    task_id = data["task_id"]
    print("✓ Task submitted successfully")
    print(f"  Task ID: {task_id}")
    print(f"  Status: {data['status']}")
    print(f"  Message: {data['message']}")

    return task_id


def poll_task_status(task_id: str, max_wait: int = MAX_WAIT_TIME) -> Dict[str, Any]:
    """Poll task status until completed or failed"""
    print("\n=== Polling Task Status ===")
    print(f"Task ID: {task_id}")
    print(f"Max wait time: {max_wait}s")

    start_time = time.time()
    poll_count = 0

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(f"Task did not complete within {max_wait}s")

        poll_count += 1
        response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200, f"Status check failed: {response.status_code}"

        data = response.json()
        status = data["status"]
        progress = data.get("progress", "")

        print(f"  Poll #{poll_count} ({elapsed:.1f}s): {status} - {progress}")

        if status in ["completed", "failed"]:
            print(f"\n✓ Task reached terminal state: {status}")
            if data.get("error"):
                print(f"  Error: {data['error']}")
            return data

        time.sleep(POLL_INTERVAL)


def get_task_result(task_id: str) -> Dict[str, Any]:
    """Retrieve the final task result"""
    print("\n=== Retrieving Task Result ===")

    response = requests.get(f"{API_BASE_URL}/tasks/{task_id}/result")

    if response.status_code == 409:
        print("✗ Task not yet completed")
        return None

    assert response.status_code == 200, f"Result retrieval failed: {response.status_code}"

    data = response.json()
    print("✓ Result retrieved successfully")
    print(f"  Success: {data['success']}")
    print(f"  Execution time: {data['execution_time']:.2f}s")
    print(f"  Artifacts: {len(data['artifacts'])}")
    print(f"  Validation passed: {data['validation']['passed']}")

    return data


def validate_result(result: Dict[str, Any], expected_success: bool = True):
    """Validate the result structure and content"""
    print("\n=== Validating Result ===")

    # Check success status
    assert "success" in result, "Missing 'success' field"
    assert result["success"] == expected_success, f"Expected success={expected_success}, got {result['success']}"
    print(f"✓ Success status matches expectation: {expected_success}")

    # Check artifacts
    assert "artifacts" in result, "Missing 'artifacts' field"
    artifacts = result["artifacts"]
    print(f"✓ Artifacts present: {len(artifacts)}")

    if artifacts:
        for i, artifact in enumerate(artifacts, 1):
            print(f"  Artifact {i}:")
            print(f"    - Type: {artifact['content_type']}")
            print(f"    - Created by: {artifact['created_by']}")
            if artifact["content_type"] == "text":
                content_preview = str(artifact["content"])[:100]
                print(f"    - Content preview: {content_preview}...")

    # Check validation
    assert "validation" in result, "Missing 'validation' field"
    validation = result["validation"]
    print("✓ Validation present")
    print(f"  - Passed: {validation['passed']}")
    print(f"  - Confidence: {validation['confidence']:.2f}")
    print(f"  - Checks: {len(validation['checks'])}")
    print(f"  - Issues: {len(validation['issues'])}")

    if validation["issues"]:
        print("  Issues found:")
        for issue in validation["issues"]:
            print(f"    - [{issue['severity']}] {issue['description']}")

    # Check execution plan
    assert "plan" in result, "Missing 'plan' field"
    plan = result["plan"]
    print(f"✓ Execution plan present: {len(plan['steps'])} steps")

    print("\n✓ All validations passed!")


def run_simple_task_test():
    """Run a complete test with a simple task"""
    print("\n" + "=" * 60)
    print("INTEGRATION TEST: Simple Python Hello World")
    print("=" * 60)

    # 1. Check API health
    test_api_health()

    # 2. Submit task
    task_id = submit_task(
        goal="Create a Python file that prints 'Hello, World!'", context={"language": "python", "filename": "hello.py"}
    )

    # 3. Poll for completion
    status = poll_task_status(task_id, max_wait=120)  # 2 minutes for full execution

    # 4. Retrieve result
    result = get_task_result(task_id)

    # 5. Validate result
    validate_result(result, expected_success=True)

    print("\n" + "=" * 60)
    print("✓ INTEGRATION TEST PASSED")
    print("=" * 60)


def run_all_tests():
    """Run all integration tests"""
    try:
        run_simple_task_test()

        # Add more test cases here
        # run_complex_task_test()
        # run_failure_case_test()

        print("\n✓ All integration tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting API Integration Tests...")
    print(f"Target: {API_BASE_URL}")
    print("\nNOTE: Ensure the API server is running before executing tests.")
    print("      Start with: python -m src.api\n")

    input("Press Enter to continue...")

    success = run_all_tests()
    exit(0 if success else 1)
