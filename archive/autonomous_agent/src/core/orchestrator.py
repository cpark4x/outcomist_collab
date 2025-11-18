"""
Orchestrator: Coordinates the P→E→V workflow for task execution.

This module is the main coordinator that:
- Creates working memory for each task
- Orchestrates Planner → Executor → Verifier flow
- Handles error recovery and retries
- Returns consolidated TaskResult

Contract:
    Inputs: TaskIntent
    Outputs: TaskResult
    Side Effects: Creates working memory, orchestrates agents, LLM API calls

Design Philosophy:
- Clear separation: Orchestration logic, not implementation
- Error recovery: Retry planning on execution failure
- Full auditability: All decisions logged and stored in memory
- Ruthless simplicity: Direct flow without over-abstraction
"""

import logging
import time
import uuid
from datetime import datetime

from ..agents.executor import ExecutionError, ExecutorAgent
from ..agents.planner import PlannerAgent
from ..agents.verifier import VerifierAgent
from .contracts import ExecutionPlan, TaskIntent, TaskResult, ValidationResult
from .working_memory import WorkingMemory

logger = logging.getLogger(__name__)


class OrchestrationError(Exception):
    """Raised when orchestration fails"""

    pass


class Orchestrator:
    """
    Coordinates the autonomous agent P→E→V workflow.

    Responsibilities:
    1. Initialize working memory for task
    2. Plan: TaskIntent → ExecutionPlan (via Planner)
    3. Execute: ExecutionPlan → Artifacts (via Executor)
    4. Verify: Artifacts → ValidationResult (via Verifier)
    5. Return: TaskResult to user

    Error Recovery:
    - Planning failure → Retry with exponential backoff
    - Execution failure → Attempt replan (1 retry)
    - Verification failure → Return result with issues flagged
    """

    def __init__(
        self,
        anthropic_api_key: str,
        memory_dir: str = "./memory",
        max_replan_attempts: int = 1,
    ):
        """
        Initialize the orchestrator with agent instances.

        Args:
            anthropic_api_key: API key for Claude
            memory_dir: Directory for working memory storage
            max_replan_attempts: Maximum times to replan after execution failure
        """
        self.planner = PlannerAgent(api_key=anthropic_api_key)
        self.verifier = VerifierAgent(api_key=anthropic_api_key)
        self.memory_dir = memory_dir
        self.max_replan_attempts = max_replan_attempts

        logger.info("Orchestrator initialized")

    async def execute_task(self, intent: TaskIntent) -> TaskResult:
        """
        Execute a task through the full P→E→V workflow.

        Flow:
        1. Create working memory
        2. Planner: Generate execution plan
        3. Executor: Execute steps and generate artifacts
        4. Verifier: Independently validate artifacts
        5. Return result with all context

        Args:
            intent: User's task description and requirements

        Returns:
            TaskResult with artifacts, validation, and execution metadata

        Raises:
            OrchestrationError: If workflow fails after all retries
        """
        # Generate task_id if not provided
        if not intent.task_id:
            intent.task_id = str(uuid.uuid4())

        task_id = intent.task_id
        start_time = time.time()

        logger.info(f"Starting task execution: {task_id}")
        logger.info(f"Goal: {intent.goal}")

        try:
            # 1. Initialize working memory
            memory = WorkingMemory(task_id=task_id, memory_dir=self.memory_dir)
            logger.info(f"Created working memory at {memory.db_path}")

            # 2. Planning phase
            logger.info("=== PLANNING PHASE ===")
            plan = self._plan_with_retry(intent)
            memory.store_plan(plan, status="planned")
            logger.info(f"Plan generated with {len(plan.steps)} steps")

            # 3. Execution phase (with replan on failure)
            logger.info("=== EXECUTION PHASE ===")
            artifacts = self._execute_with_replan(plan, intent, memory, max_attempts=self.max_replan_attempts + 1)
            logger.info(f"Execution completed: {len(artifacts)} artifacts generated")

            # 4. Verification phase
            logger.info("=== VERIFICATION PHASE ===")
            validation = self.verifier.verify_plan_completion(
                artifacts=artifacts,
                criteria=plan.success_criteria,
                task_goal=intent.goal,
            )
            memory.store_validation(validation)

            if validation.passed:
                logger.info("✓ Verification PASSED")
            else:
                logger.warning(f"✗ Verification FAILED: {len(validation.issues)} issues found")
                for issue in validation.issues:
                    logger.warning(f"  - [{issue.severity}] {issue.description}")

            # 5. Build final result
            execution_time = time.time() - start_time
            result = TaskResult(
                task_id=task_id,
                success=validation.passed,
                artifacts=artifacts,
                validation=validation,
                execution_time=execution_time,
                plan=plan,
                completed_at=datetime.utcnow(),
                error=None,
            )

            logger.info(f"Task {task_id} completed in {execution_time:.2f}s")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Orchestration failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            # Return failed result with error details
            return TaskResult(
                task_id=task_id,
                success=False,
                artifacts=[],
                validation=ValidationResult(passed=False, checks=[], issues=[], confidence=0.0),
                execution_time=execution_time,
                plan=ExecutionPlan(task_id=task_id, steps=[], success_criteria={}, estimated_duration=0),
                completed_at=datetime.utcnow(),
                error=error_msg,
            )

    def _plan_with_retry(self, intent: TaskIntent) -> ExecutionPlan:
        """
        Generate execution plan with retry logic.

        Strategy: Planner.plan() already has internal retry logic,
        so we just call it once. If it fails after its retries,
        we let the error propagate.

        Args:
            intent: Task intent

        Returns:
            ExecutionPlan

        Raises:
            OrchestrationError: If planning fails
        """
        try:
            return self.planner.plan(intent)
        except Exception as e:
            raise OrchestrationError(f"Planning failed: {str(e)}") from e

    def _execute_with_replan(
        self,
        plan: ExecutionPlan,
        original_intent: TaskIntent,
        memory: WorkingMemory,
        max_attempts: int,
    ) -> list:
        """
        Execute plan with replan on failure.

        Strategy:
        1. Try to execute the plan
        2. If execution fails, attempt replan (once)
        3. Execute the new plan
        4. If still fails, raise error

        Args:
            plan: Initial execution plan
            original_intent: Original user intent (for replanning)
            memory: Working memory
            max_attempts: Maximum execution attempts

        Returns:
            List of artifacts

        Raises:
            OrchestrationError: If execution fails after all attempts
        """
        current_plan = plan
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"Execution attempt {attempt}/{max_attempts}")

                # Create executor with this memory
                executor = ExecutorAgent(memory=memory)

                # Execute plan
                artifacts = executor.execute_plan(current_plan)

                logger.info(f"Execution successful on attempt {attempt}")
                return artifacts

            except ExecutionError as e:
                last_error = e
                logger.warning(f"Execution attempt {attempt} failed: {str(e)}")

                if attempt < max_attempts:
                    # Attempt replan
                    logger.info("Attempting to replan after execution failure...")

                    try:
                        # Get the failed step from error message
                        # This is simplified - in production, pass the actual failed step
                        failed_step = current_plan.steps[0]  # Placeholder: get actual failed step

                        current_plan = self.planner.replan(
                            failed_step=failed_step,
                            error=str(e),
                            memory=memory,
                            original_intent=original_intent,
                        )

                        memory.store_plan(current_plan, status="replanned")
                        logger.info(f"Replanning successful: {len(current_plan.steps)} new steps")

                    except Exception as replan_error:
                        logger.error(f"Replanning failed: {str(replan_error)}")
                        raise OrchestrationError(
                            f"Execution failed and replanning failed: {str(replan_error)}"
                        ) from replan_error
                else:
                    logger.error(f"All {max_attempts} execution attempts exhausted")

        # All attempts failed
        raise OrchestrationError(f"Execution failed after {max_attempts} attempts: {str(last_error)}")
