"""
Verifier Agent: Independent validation of execution outputs.

Purpose: Validate artifacts without seeing Executor's reasoning.
Contract:
  - Inputs: Artifact, expected output schema, success criteria
  - Outputs: ValidationResult
  - Side Effects: LLM API calls (Claude)

Key Principles:
  - Stateless validation (no internal state)
  - Independence from Executor (no access to reasoning)
  - Multiple verification types (schema, logical, structural)
  - Detailed issue reporting with confidence scoring
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, List, Optional

from anthropic import Anthropic

from ..core.contracts import (
    Artifact,
    Check,
    Issue,
    ValidationResult,
)

VERIFIER_SYSTEM_PROMPT = """You are an independent verification agent. Your role is to assess whether outputs logically achieve stated goals.

You must:
1. Assess if the output logically achieves the goal
2. Check for internal contradictions
3. Evaluate completeness
4. Identify gaps or errors
5. Consider ONLY what was created, NOT how it was created

You should be thorough but fair. Output JSON with:
{
  "passed": boolean,
  "reasoning": "detailed explanation",
  "contradictions": ["list of any contradictions found"],
  "gaps": ["list of any completeness gaps"],
  "confidence": 0.0 to 1.0
}"""


class VerifierAgent:
    """
    Independently validates execution outputs.

    The Verifier operates without access to Executor's reasoning,
    ensuring true independent validation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Verifier with Claude API access.

        Args:
            api_key: Anthropic API key (uses env var if not provided)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def verify(
        self,
        artifact: Artifact,
        expected: dict[str, Any],
        context: dict[str, Any],
    ) -> ValidationResult:
        """
        Validate a single artifact.

        Args:
            artifact: The artifact to verify
            expected: Expected output schema/structure
            context: Original task context (intent, constraints)

        Returns:
            ValidationResult with checks, issues, and confidence score
        """
        checks: List[Check] = []
        issues: List[Issue] = []

        # Run verification checks
        schema_check = self._schema_check(artifact, expected)
        checks.append(schema_check)
        if not schema_check.passed:
            issues.extend(self._check_to_issues(schema_check, artifact.artifact_id))

        logical_check = self._logical_check(artifact, expected, context)
        checks.append(logical_check)
        if not logical_check.passed:
            issues.extend(self._check_to_issues(logical_check, artifact.artifact_id))

        structural_check = self._structural_check(artifact)
        checks.append(structural_check)
        if not structural_check.passed:
            issues.extend(self._check_to_issues(structural_check, artifact.artifact_id))

        # Compute overall result
        all_passed = all(c.passed for c in checks)
        confidence = self._compute_confidence(checks)

        return ValidationResult(
            passed=all_passed,
            checks=checks,
            issues=issues,
            confidence=confidence,
        )

    def verify_plan_completion(
        self,
        artifacts: List[Artifact],
        criteria: dict[str, Any],
        task_goal: str,
    ) -> ValidationResult:
        """
        Validate that all artifacts together satisfy task completion criteria.

        Args:
            artifacts: All artifacts produced during execution
            criteria: Success criteria from ExecutionPlan
            task_goal: Original task goal

        Returns:
            ValidationResult for overall task completion
        """
        checks: List[Check] = []
        issues: List[Issue] = []

        # Check completeness: are all required artifacts present?
        completeness_check = self._completeness_check(artifacts, criteria)
        checks.append(completeness_check)
        if not completeness_check.passed:
            issues.extend(self._check_to_issues(completeness_check, None))

        # Check goal achievement: do artifacts satisfy the task goal?
        goal_check = self._goal_achievement_check(artifacts, task_goal, criteria)
        checks.append(goal_check)
        if not goal_check.passed:
            issues.extend(self._check_to_issues(goal_check, None))

        all_passed = all(c.passed for c in checks)
        confidence = self._compute_confidence(checks)

        return ValidationResult(
            passed=all_passed,
            checks=checks,
            issues=issues,
            confidence=confidence,
        )

    def _schema_check(
        self,
        artifact: Artifact,
        expected: dict[str, Any],
    ) -> Check:
        """
        Validate artifact matches expected schema.

        Uses JSON schema-style validation for structure matching.
        """
        try:
            # Check content type matches
            expected_type = expected.get("content_type")
            if expected_type and artifact.content_type != expected_type:
                return Check(
                    check_type="schema",
                    passed=False,
                    details=f"Content type mismatch: expected {expected_type}, got {artifact.content_type}",
                    confidence=1.0,
                )

            # Check required fields if specified
            required_fields = expected.get("required_fields", [])
            if required_fields and isinstance(artifact.content, dict):
                missing = [f for f in required_fields if f not in artifact.content]
                if missing:
                    return Check(
                        check_type="schema",
                        passed=False,
                        details=f"Missing required fields: {missing}",
                        confidence=1.0,
                    )

            # Check structure if JSON schema provided
            if "schema" in expected:
                validation_errors = self._validate_json_schema(artifact.content, expected["schema"])
                if validation_errors:
                    return Check(
                        check_type="schema",
                        passed=False,
                        details=f"Schema validation errors: {validation_errors}",
                        confidence=1.0,
                    )

            return Check(
                check_type="schema",
                passed=True,
                details="Artifact matches expected schema",
                confidence=1.0,
            )

        except Exception as e:
            return Check(
                check_type="schema",
                passed=False,
                details=f"Schema validation failed: {str(e)}",
                confidence=0.5,
            )

    def _logical_check(
        self,
        artifact: Artifact,
        expected: dict[str, Any],
        context: dict[str, Any],
    ) -> Check:
        """
        Use Claude to assess logical consistency and goal achievement.

        This is the core "reasoning verification" step.
        """
        try:
            # Prepare verification prompt
            prompt = self._build_logical_verification_prompt(artifact, expected, context)

            # Get Claude's assessment
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=VERIFIER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            result_text = response.content[0].text
            result = self._parse_llm_json(result_text)

            return Check(
                check_type="logical",
                passed=result.get("passed", False),
                details=result.get("reasoning", "No reasoning provided"),
                confidence=result.get("confidence", 0.5),
                evidence={
                    "contradictions": result.get("contradictions", []),
                    "gaps": result.get("gaps", []),
                },
            )

        except Exception as e:
            return Check(
                check_type="logical",
                passed=False,
                details=f"Logical check failed: {str(e)}",
                confidence=0.3,
            )

    def _structural_check(self, artifact: Artifact) -> Check:
        """
        Validate structural integrity (code runs, files exist, etc.).

        Performs actual execution/existence checks.
        """
        try:
            if artifact.content_type == "code":
                return self._validate_code_execution(artifact)
            elif artifact.content_type == "file_path":
                return self._validate_file_exists(artifact)
            elif artifact.content_type == "json":
                return self._validate_json_parseable(artifact)
            else:
                # No structural validation for other types
                return Check(
                    check_type="structural",
                    passed=True,
                    details=f"No structural check for type {artifact.content_type}",
                    confidence=1.0,
                )

        except Exception as e:
            return Check(
                check_type="structural",
                passed=False,
                details=f"Structural check failed: {str(e)}",
                confidence=0.5,
            )

    def _completeness_check(
        self,
        artifacts: List[Artifact],
        criteria: dict[str, Any],
    ) -> Check:
        """Check if all required artifacts are present."""
        required_artifacts = criteria.get("required_artifacts", [])

        if not required_artifacts:
            return Check(
                check_type="completeness",
                passed=True,
                details="No specific artifacts required",
                confidence=1.0,
            )

        artifact_types = {a.content_type for a in artifacts}
        missing = [req for req in required_artifacts if req not in artifact_types]

        if missing:
            return Check(
                check_type="completeness",
                passed=False,
                details=f"Missing required artifacts: {missing}",
                confidence=1.0,
            )

        return Check(
            check_type="completeness",
            passed=True,
            details=f"All required artifacts present: {list(artifact_types)}",
            confidence=1.0,
        )

    def _goal_achievement_check(
        self,
        artifacts: List[Artifact],
        task_goal: str,
        criteria: dict[str, Any],
    ) -> Check:
        """Use Claude to assess if artifacts collectively achieve the task goal."""
        try:
            prompt = f"""Task Goal: {task_goal}

Success Criteria: {json.dumps(criteria, indent=2)}

Artifacts Produced:
{self._format_artifacts_summary(artifacts)}

Question: Do these artifacts collectively achieve the stated task goal?
Consider:
1. Does the output logically satisfy the goal?
2. Are there obvious gaps in functionality?
3. Is the solution complete enough to be useful?

Respond with JSON."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=VERIFIER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )

            result_text = response.content[0].text
            result = self._parse_llm_json(result_text)

            return Check(
                check_type="goal_achievement",
                passed=result.get("passed", False),
                details=result.get("reasoning", "No reasoning provided"),
                confidence=result.get("confidence", 0.5),
                evidence={
                    "gaps": result.get("gaps", []),
                },
            )

        except Exception as e:
            return Check(
                check_type="goal_achievement",
                passed=False,
                details=f"Goal achievement check failed: {str(e)}",
                confidence=0.3,
            )

    # Helper methods

    def _validate_code_execution(self, artifact: Artifact) -> Check:
        """Try to execute code and check for errors."""
        code = artifact.content
        language = artifact.metadata.get("language", "python")

        if language != "python":
            return Check(
                check_type="structural",
                passed=True,
                details=f"Code execution validation not supported for {language}",
                confidence=0.5,
            )

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=5,
            )

            Path(temp_path).unlink()

            if result.returncode != 0:
                return Check(
                    check_type="structural",
                    passed=False,
                    details=f"Code execution failed: {result.stderr}",
                    confidence=0.9,
                )

            return Check(
                check_type="structural",
                passed=True,
                details="Code executes without errors",
                confidence=0.9,
            )

        except subprocess.TimeoutExpired:
            return Check(
                check_type="structural",
                passed=False,
                details="Code execution timed out",
                confidence=0.8,
            )
        except Exception as e:
            return Check(
                check_type="structural",
                passed=False,
                details=f"Code validation error: {str(e)}",
                confidence=0.5,
            )

    def _validate_file_exists(self, artifact: Artifact) -> Check:
        """Check if file path exists."""
        file_path = artifact.content

        if not isinstance(file_path, str):
            return Check(
                check_type="structural",
                passed=False,
                details="File path is not a string",
                confidence=1.0,
            )

        path = Path(file_path)
        if not path.exists():
            return Check(
                check_type="structural",
                passed=False,
                details=f"File does not exist: {file_path}",
                confidence=1.0,
            )

        return Check(
            check_type="structural",
            passed=True,
            details=f"File exists: {file_path}",
            confidence=1.0,
        )

    def _validate_json_parseable(self, artifact: Artifact) -> Check:
        """Check if JSON content is valid."""
        try:
            if isinstance(artifact.content, str):
                json.loads(artifact.content)
            # If already parsed, it's valid
            return Check(
                check_type="structural",
                passed=True,
                details="JSON is valid",
                confidence=1.0,
            )
        except json.JSONDecodeError as e:
            return Check(
                check_type="structural",
                passed=False,
                details=f"Invalid JSON: {str(e)}",
                confidence=1.0,
            )

    def _validate_json_schema(self, content: Any, schema: dict[str, Any]) -> List[str]:
        """
        Simple JSON schema validation.

        Returns list of validation errors (empty if valid).
        """
        errors = []

        # Type check
        expected_type = schema.get("type")
        if expected_type:
            actual_type = type(content).__name__
            type_map = {
                "object": "dict",
                "array": "list",
                "string": "str",
                "number": "float",
                "integer": "int",
                "boolean": "bool",
            }
            python_type = type_map.get(expected_type, expected_type)
            if actual_type != python_type and not isinstance(content, eval(python_type)):
                errors.append(f"Expected type {expected_type}, got {actual_type}")

        # Required properties for objects
        if isinstance(content, dict) and "required" in schema:
            for prop in schema["required"]:
                if prop not in content:
                    errors.append(f"Missing required property: {prop}")

        return errors

    def _build_logical_verification_prompt(
        self,
        artifact: Artifact,
        expected: dict[str, Any],
        context: dict[str, Any],
    ) -> str:
        """Build prompt for logical consistency check."""
        return f"""Expected Output: {json.dumps(expected, indent=2)}

Task Context: {json.dumps(context, indent=2)}

Actual Output:
Content Type: {artifact.content_type}
Content: {self._format_content(artifact.content)}

Question: Does this output logically achieve what was expected given the task context?

Evaluate:
1. Does it solve the problem described in the context?
2. Are there logical contradictions in the output?
3. Is it complete enough to be considered successful?
4. Are there obvious errors or gaps?

Respond with JSON following the schema."""

    def _format_content(self, content: Any, max_length: int = 1000) -> str:
        """Format content for display in prompts."""
        if isinstance(content, str):
            if len(content) > max_length:
                return content[:max_length] + f"... (truncated, {len(content)} chars total)"
            return content
        elif isinstance(content, (dict, list)):
            content_str = json.dumps(content, indent=2)
            if len(content_str) > max_length:
                return content_str[:max_length] + "... (truncated)"
            return content_str
        else:
            return str(content)

    def _format_artifacts_summary(self, artifacts: List[Artifact]) -> str:
        """Format artifacts for summary display."""
        summary = []
        for i, artifact in enumerate(artifacts, 1):
            summary.append(
                f"{i}. Type: {artifact.content_type}, Content: {self._format_content(artifact.content, max_length=200)}"
            )
        return "\n".join(summary)

    def _parse_llm_json(self, text: str) -> dict[str, Any]:
        """
        Parse JSON from LLM response, handling markdown wrapping.

        Extracts JSON even if wrapped in markdown code blocks.
        """
        text = text.strip()

        # Remove markdown code blocks
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json or ````)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)

        return json.loads(text)

    def _compute_confidence(self, checks: List[Check]) -> float:
        """
        Compute overall confidence score from individual checks.

        Uses weighted average based on check types.
        """
        if not checks:
            return 0.0

        # Weight different check types
        weights = {
            "schema": 1.0,
            "logical": 1.5,  # Logical checks are most important
            "structural": 1.0,
            "completeness": 1.2,
            "goal_achievement": 1.5,
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for check in checks:
            weight = weights.get(check.check_type, 1.0)
            # Failed checks contribute 0, passed checks contribute their confidence
            contribution = check.confidence if check.passed else 0.0
            weighted_sum += contribution * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _check_to_issues(self, check: Check, artifact_id: Optional[str]) -> List[Issue]:
        """Convert a failed check into Issues."""
        if check.passed:
            return []

        # Determine severity based on check type and confidence
        if check.check_type in ["schema", "structural"]:
            severity = "critical"
        elif check.check_type == "logical" and check.confidence > 0.7:
            severity = "major"
        elif check.check_type == "goal_achievement":
            severity = "critical"
        else:
            severity = "minor"

        issue = Issue(
            severity=severity,
            description=f"{check.check_type.title()} check failed: {check.details}",
            artifact_id=artifact_id,
            recommendation=self._generate_recommendation(check),
        )

        return [issue]

    def _generate_recommendation(self, check: Check) -> str:
        """Generate recommendation based on failed check."""
        if check.check_type == "schema":
            return "Review expected schema and ensure artifact structure matches"
        elif check.check_type == "logical":
            gaps = check.evidence.get("gaps", [])
            contradictions = check.evidence.get("contradictions", [])
            recommendations = []
            if gaps:
                recommendations.append(f"Address gaps: {', '.join(gaps)}")
            if contradictions:
                recommendations.append(f"Resolve contradictions: {', '.join(contradictions)}")
            return " | ".join(recommendations) if recommendations else "Review logic"
        elif check.check_type == "structural":
            return "Fix structural issues in artifact (syntax, execution, existence)"
        elif check.check_type == "completeness":
            return "Ensure all required artifacts are generated"
        elif check.check_type == "goal_achievement":
            return "Review artifacts to ensure they fully address the task goal"
        else:
            return "Review and address validation failure"
