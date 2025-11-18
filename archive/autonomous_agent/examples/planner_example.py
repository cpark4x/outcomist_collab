"""
Example usage of the Planner Agent.

This script demonstrates:
1. Creating a TaskIntent
2. Generating an ExecutionPlan
3. Inspecting the plan structure
4. Understanding dependencies
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.planner import PlannerAgent
from src.core.contracts import TaskIntent


def main():
    """Demonstrate planner usage"""

    # Step 1: Create a task intent
    print("=" * 60)
    print("Step 1: Create TaskIntent")
    print("=" * 60)

    intent = TaskIntent(
        goal="Create a Python file that calculates fibonacci(10)",
        context={"language": "python", "function_name": "fibonacci", "output_path": "./fibonacci.py"},
        constraints={"max_execution_time": 600, "max_steps": 5},
        task_id="example_task_001",
        user_id="demo_user",
    )

    print(f"Goal: {intent.goal}")
    print(f"Context: {intent.context}")
    print(f"Constraints: {intent.constraints}")
    print()

    # Step 2: Initialize planner
    print("=" * 60)
    print("Step 2: Initialize Planner Agent")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Warning: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your_key_here'")
        print()
        print("For this example, we'll show what the planner would do...")
        print()
        demonstrate_without_api()
        return

    planner = PlannerAgent(api_key=api_key)
    print(f"Model: {planner.model}")
    print(f"Max retries: {planner.max_retries}")
    print()

    # Step 3: Generate plan
    print("=" * 60)
    print("Step 3: Generate Execution Plan")
    print("=" * 60)

    try:
        plan = planner.plan(intent)

        print(f"Task ID: {plan.task_id}")
        print(f"Total steps: {len(plan.steps)}")
        print(f"Estimated duration: {plan.estimated_duration}s")
        print()

        # Step 4: Inspect steps
        print("=" * 60)
        print("Step 4: Inspect Generated Steps")
        print("=" * 60)

        for i, step in enumerate(plan.steps, 1):
            print(f"\n[Step {i}] {step.step_id}")
            print(f"  Tool: {step.tool.value}")
            print(f"  Timeout: {step.timeout}s")
            print(f"  Dependencies: {step.dependencies or 'None'}")
            print(f"  Inputs: {step.inputs}")
            print(f"  Expected output: {step.expected_output}")

        print()

        # Step 5: Show success criteria
        print("=" * 60)
        print("Step 5: Success Criteria")
        print("=" * 60)

        criteria = plan.success_criteria
        print("\nPrimary criteria:")
        for criterion in criteria.get("primary", []):
            print(f"  ✓ {criterion}")

        print("\nValidation checks:")
        for check in criteria.get("validation", []):
            print(f"  ✓ {check}")

        print()

        # Step 6: Demonstrate ready steps
        print("=" * 60)
        print("Step 6: Identify Ready Steps")
        print("=" * 60)

        ready_steps = plan.get_ready_steps()
        print(f"\nSteps ready to execute: {len(ready_steps)}")
        for step in ready_steps:
            print(f"  → {step.step_id} (no pending dependencies)")

        print()
        print("✅ Plan generation successful!")

    except Exception as e:
        print(f"❌ Error generating plan: {e}")
        return 1

    return 0


def demonstrate_without_api():
    """Show what the planner output looks like without calling the API"""

    print("=" * 60)
    print("Example Plan Structure (without API call)")
    print("=" * 60)

    print("""
ExecutionPlan:
  task_id: example_task_001
  estimated_duration: 900s

  Steps:
    [1] step_1
        Tool: research
        Dependencies: None
        Purpose: Research fibonacci algorithm implementation

    [2] step_2
        Tool: code_exec
        Dependencies: step_1
        Purpose: Write and test fibonacci function

    [3] step_3
        Tool: filesystem
        Dependencies: step_2
        Purpose: Save code to fibonacci.py

  Success Criteria:
    Primary:
      ✓ File exists at ./fibonacci.py
      ✓ Code runs without errors
      ✓ fibonacci(10) returns 55

    Validation:
      ✓ Python syntax is valid
      ✓ Function is properly defined
      ✓ Code includes docstring
""")

    print("\nTo see actual plan generation, set ANTHROPIC_API_KEY environment variable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
