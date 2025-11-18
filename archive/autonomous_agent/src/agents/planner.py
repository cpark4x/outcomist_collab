"""
Planner Agent: Convert TaskIntent into ExecutionPlan.

This module is responsible for breaking down user intentions into
executable plans with clear dependencies, tool requirements, and success criteria.

Design Philosophy:
- Ruthless simplicity: Generate 3-5 step plans for MVP
- Clear contracts: Well-defined inputs/outputs via TaskIntent and ExecutionPlan
- Graceful errors: Retry with exponential backoff, informative error messages
- Auditability: Log all planning decisions for debugging

Contract:
    Inputs: TaskIntent (user goal + context)
    Outputs: ExecutionPlan (steps with dependencies)
    Side Effects: LLM API calls (Claude via anthropic SDK)
"""

import logging
import time
import uuid
from datetime import datetime
from typing import List

from anthropic import Anthropic

from ..core.contracts import (
    ExecutionPlan,
    Step,
    StepStatus,
    TaskIntent,
    ToolType,
)
from ..core.working_memory import WorkingMemory

logger = logging.getLogger(__name__)


# Planning prompt template
SYSTEM_PROMPT = """You are a task planning expert. Your role is to break down user tasks into 3-5 executable steps.

For each step, you must:
1. Identify the appropriate tool (code_exec, filesystem, research, browser, image_gen)
2. Define clear inputs required for execution
3. Specify expected output structure (JSON schema)
4. List dependencies on other steps (by step_id)
5. Estimate reasonable timeout (default 300s)

Guidelines:
- Keep it simple: 3-5 steps maximum for MVP
- Be specific: Clear, actionable steps that can be executed independently
- Define dependencies: Step N can depend on steps 1..(N-1) only
- Specify success criteria: Measurable outcomes that define task completion
- Estimate duration: Realistic time estimates for each step

CRITICAL: Return ONLY valid JSON. No trailing commas, no comments, no markdown unless explicitly wrapping JSON.

Available tools:
- code_exec: Execute PYTHON code ONLY (uses Python exec()). Can write files directly using open().
- filesystem: Read, write, delete files and directories (use for simple file operations).
- research: Search web, query knowledge bases, gather information
- browser: (Future V1.0) Navigate web pages, extract content
- image_gen: (Future V1.0) Generate images from text descriptions

IMPORTANT: For HTML/JS/CSS generation tasks, use code_exec to generate AND write files in ONE step:

Example:
{
  "steps": [
    {
      "step_id": "step_1",
      "tool": "code_exec",
      "inputs": {
        "code": "html_content = '''<!DOCTYPE html>\\n<html>...complete HTML with all features...</html>'''\\n\\nwith open('game.html', 'w') as f:\\n    f.write(html_content)\\n\\nprint(f'Successfully wrote {len(html_content)} characters to game.html')"
      },
      "expected_output": {"type": "object", "properties": {"stdout": {"type": "string"}, "success": {"type": "boolean"}}},
      "timeout": 300,
      "dependencies": []
    }
  ]
}

Output format (JSON):
{
  "steps": [
    {
      "step_id": "step_1",
      "tool": "research",
      "inputs": {"query": "...", "sources": [...]},
      "expected_output": {"type": "object", "properties": {...}},
      "timeout": 300,
      "dependencies": []
    },
    ...
  ],
  "success_criteria": {
    "primary": ["criterion 1", "criterion 2"],
    "validation": ["check 1", "check 2"]
  },
  "estimated_duration": 600
}"""


class PlannerAgent:
    """
    Planner Agent: Converts user intent into detailed execution plans.

    Responsibilities:
    1. Analyze TaskIntent to understand user goals
    2. Generate 3-5 step ExecutionPlan with clear dependencies
    3. Define success criteria and validation checks
    4. Handle replanning when steps fail

    Usage:
        planner = PlannerAgent(api_key="...")
        plan = planner.plan(intent)

        # If step fails:
        new_plan = planner.replan(failed_step, error_msg, memory)
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", max_retries: int = 3):
        """
        Initialize the Planner Agent.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
            max_retries: Maximum retry attempts for API calls
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_retries = max_retries

    def plan(self, intent: TaskIntent) -> ExecutionPlan:
        """
        Generate an execution plan from user intent.

        Strategy:
        1. Construct planning prompt with user goal and context
        2. Call Claude API to generate plan structure
        3. Parse response into ExecutionPlan
        4. Validate plan (dependencies, tool availability)
        5. Return plan ready for execution

        Args:
            intent: User's task description and requirements

        Returns:
            ExecutionPlan with 3-5 executable steps

        Raises:
            ValueError: If plan generation fails after retries
            RuntimeError: If API is unavailable
        """
        logger.info(f"Generating plan for task: {intent.task_id}")
        logger.debug(f"Goal: {intent.goal}")
        logger.debug(f"Context: {intent.context}")

        # Construct user prompt
        user_prompt = self._build_planning_prompt(intent)

        # Call Claude API with retries
        plan_json = self._call_claude_with_retry(user_prompt)

        # Parse into ExecutionPlan
        plan = self._parse_plan_response(plan_json, intent.task_id or str(uuid.uuid4()))

        logger.info(f"Generated plan with {len(plan.steps)} steps")
        logger.debug(f"Success criteria: {plan.success_criteria}")

        return plan

    def replan(
        self,
        failed_step: Step,
        error: str,
        memory: WorkingMemory,
        original_intent: TaskIntent,
    ) -> ExecutionPlan:
        """
        Regenerate plan after a step failure.

        Strategy:
        1. Analyze what went wrong with failed_step
        2. Review completed steps from memory
        3. Generate alternative approach
        4. Preserve successful work, replace failed path

        Args:
            failed_step: The step that failed
            error: Error message from execution
            memory: Working memory with execution history
            original_intent: Original user task intent

        Returns:
            New ExecutionPlan addressing the failure

        Raises:
            ValueError: If replanning fails after retries
        """
        logger.info(f"Replanning due to failure in step: {failed_step.step_id}")
        logger.debug(f"Error: {error}")

        # Gather context from memory
        completed_artifacts = memory.get_artifacts()
        completed_steps = [a.created_by for a in completed_artifacts]

        # Build replanning prompt
        user_prompt = self._build_replanning_prompt(original_intent, failed_step, error, completed_steps)

        # Call Claude API
        plan_json = self._call_claude_with_retry(user_prompt)

        # Parse new plan
        new_plan = self._parse_plan_response(plan_json, original_intent.task_id or str(uuid.uuid4()))

        logger.info(f"Generated recovery plan with {len(new_plan.steps)} steps")

        return new_plan

    def _build_planning_prompt(self, intent: TaskIntent) -> str:
        """Construct the planning prompt from user intent"""
        prompt = f"""Task: {intent.goal}

Context:
{self._format_dict(intent.context)}

Constraints:
{self._format_dict(intent.constraints)}

Please generate a 3-5 step execution plan that accomplishes this task.
Remember to:
- Use available tools appropriately
- Define clear dependencies
- Specify expected outputs
- Include success criteria
- Estimate realistic duration

Return your response as valid JSON matching the specified format."""

        return prompt

    def _build_replanning_prompt(
        self,
        intent: TaskIntent,
        failed_step: Step,
        error: str,
        completed_steps: List[str],
    ) -> str:
        """Construct replanning prompt with failure context"""
        prompt = f"""Original Task: {intent.goal}

Completed steps so far: {", ".join(completed_steps)}

Failed step: {failed_step.step_id}
Tool used: {failed_step.tool.value}
Error: {error}

Please generate a new execution plan that:
1. Acknowledges the work already completed
2. Addresses the failure with an alternative approach
3. Continues toward the original goal

Return your response as valid JSON matching the specified format."""

        return prompt

    def _call_claude_with_retry(self, user_prompt: str) -> dict:
        """
        Call Claude API with exponential backoff retry logic.

        Args:
            user_prompt: User message to send

        Returns:
            Parsed JSON response

        Raises:
            RuntimeError: If all retries fail
        """
        retry_delay = 1.0  # Start with 1 second

        for attempt in range(self.max_retries):
            try:
                logger.debug(f"API call attempt {attempt + 1}/{self.max_retries}")

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_prompt}],
                )

                # Extract text content
                content = response.content[0].text

                # Log the raw content for debugging
                logger.debug(f"Raw Claude response (first 500 chars): {content[:500]}")

                # Parse JSON response - handle markdown wrapping and malformed JSON
                import json
                import re

                # Try to extract JSON from markdown blocks
                json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
                    logger.debug("Extracted JSON from markdown block")

                # Also try to find JSON object if response has text before/after
                if not content.strip().startswith("{"):
                    json_obj_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_obj_match:
                        content = json_obj_match.group(0)
                        logger.debug("Extracted JSON object from response text")

                # Clean up common JSON issues
                content = content.strip()

                # Remove trailing commas before closing braces/brackets
                content = re.sub(r",(\s*[}\]])", r"\1", content)

                # Try parsing with standard json first
                try:
                    plan_json = json.loads(content)
                except json.JSONDecodeError as e:
                    # If standard parsing fails, log the problematic content and try repair
                    logger.warning(f"JSON parse error at position {e.pos}: {e.msg}")
                    logger.debug(f"Problematic JSON snippet: {content[max(0, e.pos - 50) : e.pos + 50]}")

                    # Try to repair common issues
                    # Remove comments (not valid in JSON)
                    content = re.sub(r"//.*?$", "", content, flags=re.MULTILINE)
                    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

                    # Try again after repair
                    plan_json = json.loads(content)

                logger.debug("Successfully parsed plan JSON")
                return plan_json

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error("All retry attempts exhausted")
                    raise RuntimeError(f"Failed to generate plan after {self.max_retries} attempts: {e}")

    def _parse_plan_response(self, plan_json: dict, task_id: str) -> ExecutionPlan:
        """
        Parse Claude's JSON response into ExecutionPlan.

        Args:
            plan_json: JSON object from Claude
            task_id: Task identifier

        Returns:
            ExecutionPlan with validated structure
        """
        steps = []

        for step_data in plan_json.get("steps", []):
            # Parse tool type
            tool_str = step_data.get("tool", "").upper()
            try:
                tool = ToolType[tool_str]
            except KeyError:
                logger.warning(f"Unknown tool type: {tool_str}, defaulting to CODE_EXEC")
                tool = ToolType.CODE_EXEC

            step = Step(
                step_id=step_data.get("step_id", f"step_{len(steps) + 1}"),
                tool=tool,
                inputs=step_data.get("inputs", {}),
                expected_output=step_data.get("expected_output", {}),
                timeout=step_data.get("timeout", 300),
                dependencies=step_data.get("dependencies", []),
                status=StepStatus.PENDING,
                created_at=datetime.utcnow(),
            )

            steps.append(step)

        plan = ExecutionPlan(
            task_id=task_id,
            steps=steps,
            success_criteria=plan_json.get("success_criteria", {}),
            estimated_duration=plan_json.get("estimated_duration", 0),
            created_at=datetime.utcnow(),
            created_by="planner",
        )

        # Validate dependencies
        self._validate_dependencies(plan)

        return plan

    def _validate_dependencies(self, plan: ExecutionPlan) -> None:
        """
        Validate that all step dependencies are valid.

        Checks:
        - Referenced steps exist
        - No circular dependencies
        - Dependencies only reference earlier steps

        Raises:
            ValueError: If dependencies are invalid
        """
        step_ids = {step.step_id for step in plan.steps}

        for step in plan.steps:
            for dep_id in step.dependencies:
                if dep_id not in step_ids:
                    raise ValueError(f"Step {step.step_id} depends on non-existent step: {dep_id}")

                # Ensure dependency comes before this step
                dep_step = plan.get_step(dep_id)
                if dep_step:
                    dep_index = plan.steps.index(dep_step)
                    step_index = plan.steps.index(step)
                    if dep_index >= step_index:
                        raise ValueError(f"Step {step.step_id} depends on later step: {dep_id}")

        logger.debug("Dependencies validated successfully")

    def _format_dict(self, d: dict) -> str:
        """Format dictionary for display in prompts"""
        if not d:
            return "(none)"
        return "\n".join(f"  - {k}: {v}" for k, v in d.items())
