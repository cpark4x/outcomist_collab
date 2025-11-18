"""
Architecture Validation Against 10 Non-Engineering Use Case Scenarios

This validates that the P→E→V architecture CAN HANDLE each scenario
by analyzing the requirements and mapping them to system capabilities.

This is a design validation test, not an integration test.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ArchitectureValidator:
    """Validates P→E→V architecture against scenario requirements"""

    def __init__(self):
        self.validation_results: List[Dict[str, Any]] = []

    def validate_scenario(
        self,
        scenario_num: int,
        user_role: str,
        goal: str,
        constraints: Dict[str, Any],
        expected_artifacts: List[str],
        verifier_checks: List[str],
    ) -> Dict[str, Any]:
        """Validate that architecture can handle this scenario"""

        print(f"\n{'=' * 80}")
        print(f"SCENARIO {scenario_num}: {user_role}")
        print(f"{'=' * 80}")
        print(f"Goal: {goal}")
        print()

        # Analyze scenario requirements
        analysis = {
            "scenario_num": scenario_num,
            "user_role": user_role,
            "goal": goal,
            "complexity_assessment": self._assess_complexity(goal, constraints),
            "planner_capability": self._can_planner_handle(goal, constraints),
            "executor_capability": self._can_executor_handle(expected_artifacts, constraints),
            "verifier_capability": self._can_verifier_handle(verifier_checks, constraints),
            "tool_gaps": self._identify_tool_gaps(expected_artifacts, constraints),
            "architecture_support": "SUPPORTED",  # Will be set based on analysis
            "recommendations": [],
        }

        # Determine if architecture supports this scenario
        planner_ok, planner_issues = analysis["planner_capability"]
        executor_ok, executor_issues = analysis["executor_capability"]
        verifier_ok, verifier_issues = analysis["verifier_capability"]

        all_ok = planner_ok and executor_ok and verifier_ok

        if not all_ok:
            analysis["architecture_support"] = "PARTIAL" if (planner_ok or executor_ok) else "NEEDS_EXTENSION"
            analysis["recommendations"] = planner_issues + executor_issues + verifier_issues
        else:
            analysis["architecture_support"] = "FULLY_SUPPORTED"

        # Print assessment
        self._print_assessment(analysis)

        self.validation_results.append(analysis)
        return analysis

    def _assess_complexity(self, goal: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Assess scenario complexity"""

        # Count complexity indicators
        indicators = {
            "multi_artifact": len(constraints.get("expected_artifacts", [])) > 1,
            "external_data": any(k in goal.lower() for k in ["csv", "data", "research", "news"]),
            "code_generation": "python" in goal.lower() or "script" in goal.lower(),
            "compliance": any(k in goal.lower() for k in ["law", "policy", "compliance", "legal"]),
            "formatting": any(k in str(constraints) for k in ["format", "slides", "apa", "csv"]),
            "verification": len(constraints.get("verifier_checks", [])) > 2,
        }

        complexity_score = sum(indicators.values())

        return {
            "score": complexity_score,
            "level": "LOW" if complexity_score <= 2 else "MEDIUM" if complexity_score <= 4 else "HIGH",
            "indicators": indicators,
        }

    def _can_planner_handle(self, goal: str, constraints: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Check if Planner can decompose this task"""

        issues = []

        # Planner needs clear goal decomposition
        if len(goal.split()) < 10:
            issues.append("Goal might be too vague for effective planning")

        # Complex multi-step workflows
        if "workflow" in goal.lower() or "automation" in goal.lower():
            # OK - Planner should handle this
            pass

        # Research tasks
        if "research" in goal.lower() or "analysis" in goal.lower():
            # OK - Can break into research steps
            pass

        # Code generation
        if "python" in goal.lower() or "script" in goal.lower():
            # OK - Can plan code generation steps
            pass

        return (len(issues) == 0, issues)

    def _can_executor_handle(
        self, expected_artifacts: List[str], constraints: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """Check if Executor has tools for required artifacts"""

        issues = []

        # Check artifact types against available tools
        available_tools = {
            "code": ["python", "py", "js", "html", "css"],
            "research": ["pdf", "md", "txt"],
            "filesystem": ["json", "csv", "xlsx", "txt", "md"],
        }

        for artifact in expected_artifacts:
            ext = artifact.split(".")[-1] if "." in artifact else ""

            # Check if we have a tool for this
            has_tool = False
            for tool_type, extensions in available_tools.items():
                if ext in extensions:
                    has_tool = True
                    break

            if not has_tool and ext:
                issues.append(f"No tool for artifact type: {artifact} (.{ext})")

        # Special cases
        if any("pptx" in a for a in expected_artifacts):
            issues.append("PowerPoint generation requires external library (not in MVP)")

        if any("xlsx" in a for a in expected_artifacts):
            issues.append("Excel generation requires external library (openpyxl - can add)")

        return (len(issues) == 0, issues)

    def _can_verifier_handle(self, verifier_checks: List[str], constraints: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Check if Verifier can validate required checks"""

        issues = []

        for check in verifier_checks:
            check_lower = check.lower()

            # Schema checks - OK (built-in)
            if "format" in check_lower or "structure" in check_lower:
                continue

            # Factual checks - OK (LLM reasoning)
            if "correct" in check_lower or "accurate" in check_lower or "match" in check_lower:
                continue

            # Count checks - OK (simple logic)
            if "exactly" in check_lower or "count" in check_lower:
                continue

            # Compliance checks - OK but requires external data
            if "compliance" in check_lower or "law" in check_lower:
                issues.append(f"Compliance check requires external legal data: {check}")

            # Performance checks - Requires external tool
            if "pagespeed" in check_lower or "performance" in check_lower:
                issues.append(f"Performance check requires external tool: {check}")

            # Integration checks - Requires external API
            if "slack" in check_lower or "jira" in check_lower:
                issues.append(f"Integration check requires external API: {check}")

        return (len(issues) == 0, issues)

    def _identify_tool_gaps(self, expected_artifacts: List[str], constraints: Dict[str, Any]) -> List[str]:
        """Identify missing tools needed for this scenario"""

        gaps = []

        # Check for special formats
        if any("pptx" in a for a in expected_artifacts):
            gaps.append("PowerPoint generation library (python-pptx)")

        if any("xlsx" in a for a in expected_artifacts):
            gaps.append("Excel library (openpyxl)")

        if any("pdf" in a for a in expected_artifacts):
            # Only gap if generating PDF (not just reading)
            if "generate" in str(constraints).lower():
                gaps.append("PDF generation library (reportlab or weasyprint)")

        # Check for external integrations
        constraints_str = str(constraints).lower()
        if "slack" in constraints_str:
            gaps.append("Slack API client")
        if "jira" in constraints_str:
            gaps.append("Jira API client")
        if "pagespeed" in constraints_str:
            gaps.append("Google PageSpeed Insights API")

        return gaps

    def _print_assessment(self, analysis: Dict[str, Any]):
        """Print scenario assessment"""

        complexity = analysis["complexity_assessment"]
        print(f"Complexity: {complexity['level']} (score: {complexity['score']}/6)")

        planner_ok, _ = analysis["planner_capability"]
        executor_ok, _ = analysis["executor_capability"]
        verifier_ok, _ = analysis["verifier_capability"]

        print("\nArchitecture Assessment:")
        print(f"  Planner:  {'✓ CAN HANDLE' if planner_ok else '✗ ISSUES'}")
        print(f"  Executor: {'✓ CAN HANDLE' if executor_ok else '✗ ISSUES'}")
        print(f"  Verifier: {'✓ CAN HANDLE' if verifier_ok else '✗ ISSUES'}")

        print(f"\nOverall Support: {analysis['architecture_support']}")

        if analysis["tool_gaps"]:
            print("\nTool Gaps Identified:")
            for gap in analysis["tool_gaps"]:
                print(f"  • {gap}")

        if analysis["recommendations"]:
            print("\nRecommendations:")
            for rec in analysis["recommendations"]:
                print(f"  • {rec}")

    def run_all_scenarios(self):
        """Validate architecture against all 10 scenarios"""

        scenarios = [
            {
                "scenario_num": 1,
                "user_role": "Product Manager",
                "goal": "Generate a competitive analysis report on Domino's and Papa John's pizza chains, including a 10-slide summary deck. Use only data from the last 18 months.",
                "constraints": {"deck_slides": 10, "data_freshness": "18 months", "output_formats": ["PDF", "PPTX"]},
                "expected_artifacts": ["competitive_analysis.pdf", "summary_deck.pptx"],
                "verifier_checks": [
                    "Exactly 10 slides in deck",
                    "All data within 18-month window",
                    "Both competitors analyzed",
                ],
            },
            {
                "scenario_num": 2,
                "user_role": "Marketing Manager",
                "goal": "Draft a launch email campaign (3 emails) for the new 'Velocity' feature. The final output must be in a single, ready-to-upload CSV file.",
                "constraints": {"email_count": 3, "output_format": "CSV"},
                "expected_artifacts": ["email_campaign.csv"],
                "verifier_checks": ["Valid CSV structure", "Exactly 3 email rows", "All required columns present"],
            },
            {
                "scenario_num": 3,
                "user_role": "Financial Analyst",
                "goal": "Generate a Python script that calculates CAGR for 3 competitors and output results to Excel with percentage formatting.",
                "constraints": {"output_formats": ["Python", "Excel"], "cagr_format": "percentage with 2 decimals"},
                "expected_artifacts": ["cagr_calculator.py", "cagr_results.xlsx"],
                "verifier_checks": [
                    "CAGR calculations mathematically correct",
                    "Excel formatting correct",
                    "Python script executable",
                ],
            },
            {
                "scenario_num": 4,
                "user_role": "HR Manager",
                "goal": "Draft a new Remote Work Policy document based on California labor law AB 1234. Output as PDF.",
                "constraints": {"compliance": "AB 1234", "output_format": "PDF"},
                "expected_artifacts": ["remote_work_policy.pdf"],
                "verifier_checks": ["AB 1234 compliance verified", "All mandatory sections present"],
            },
            {
                "scenario_num": 5,
                "user_role": "Sales Ops Manager",
                "goal": "Identify top 5 sales reps from CSV and generate personalized motivational emails with accurate revenue and rank.",
                "constraints": {"data_source": "CSV", "personalization_required": True},
                "expected_artifacts": ["rep_emails.json"],
                "verifier_checks": ["Revenue numbers match CSV", "Correct ranking (1-5)", "All 5 emails personalized"],
            },
            {
                "scenario_num": 6,
                "user_role": "Executive Assistant",
                "goal": "Write 3-sentence briefing notes for 5 external meetings with recent company news.",
                "constraints": {"sentences_per_note": 3, "meetings": 5},
                "expected_artifacts": ["meeting_briefs.md"],
                "verifier_checks": ["Exactly 3 sentences per brief", "Recent news included", "All 5 meetings covered"],
            },
            {
                "scenario_num": 7,
                "user_role": "Product Marketing Manager",
                "goal": "Generate 10 Facebook ad headlines containing 'Save 10 Hours' under 40 characters. Output as JSON.",
                "constraints": {"headline_count": 10, "required_phrase": "Save 10 Hours", "max_characters": 40},
                "expected_artifacts": ["ad_headlines.json"],
                "verifier_checks": [
                    "All headlines under 40 characters",
                    "All contain 'Save 10 Hours'",
                    "Exactly 10 unique headlines",
                ],
            },
            {
                "scenario_num": 8,
                "user_role": "Academic Researcher",
                "goal": "Summarize key findings of top 5 cited papers on ML interpretability with APA bibliography.",
                "constraints": {"citation_format": "APA 7th edition", "paper_count": 5},
                "expected_artifacts": ["ml_interpretability_bibliography.pdf"],
                "verifier_checks": ["APA formatting correct", "5 papers included", "Key findings accurate"],
            },
            {
                "scenario_num": 9,
                "user_role": "Small Business Owner",
                "goal": "Generate responsive landing page linking to Shopify that passes PageSpeed mobile score of 90+.",
                "constraints": {"pagespeed_mobile_score": 90, "shopify_link": True},
                "expected_artifacts": ["landing_page.html", "styles.css"],
                "verifier_checks": ["PageSpeed score >= 90", "Shopify URL correct", "Mobile responsive"],
            },
            {
                "scenario_num": 10,
                "user_role": "Operations Manager",
                "goal": "Create workflow automation monitoring Slack for 'URGENT', creating Jira ticket, sending confirmation.",
                "constraints": {"integrations": ["Slack", "Jira"], "trigger_keyword": "URGENT"},
                "expected_artifacts": ["workflow_automation.py"],
                "verifier_checks": [
                    "Jira ticket created with High priority",
                    "Slack confirmation sent",
                    "Keyword detection works",
                ],
            },
        ]

        print("=" * 80)
        print("ARCHITECTURE VALIDATION: 10 NON-ENGINEERING USE CASE SCENARIOS")
        print("Testing P→E→V Architecture Design Against Real-World Requirements")
        print("=" * 80)

        for scenario in scenarios:
            self.validate_scenario(**scenario)

        self._print_summary()
        self._save_results()

    def _print_summary(self):
        """Print validation summary"""

        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)

        total = len(self.validation_results)
        fully_supported = sum(1 for r in self.validation_results if r["architecture_support"] == "FULLY_SUPPORTED")
        partial = sum(1 for r in self.validation_results if r["architecture_support"] == "PARTIAL")
        needs_extension = sum(1 for r in self.validation_results if r["architecture_support"] == "NEEDS_EXTENSION")

        print("\nOverall Assessment:")
        print(f"  Total scenarios: {total}")
        print(f"  Fully supported: {fully_supported}/{total} ({fully_supported / total * 100:.0f}%)")
        print(f"  Partially supported: {partial}/{total} ({partial / total * 100:.0f}%)")
        print(f"  Needs extension: {needs_extension}/{total} ({needs_extension / total * 100:.0f}%)")

        # Complexity breakdown
        complexity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for r in self.validation_results:
            level = r["complexity_assessment"]["level"]
            complexity_counts[level] += 1

        print("\nComplexity Distribution:")
        for level, count in complexity_counts.items():
            print(f"  {level}: {count} scenarios")

        # Tool gaps summary
        all_gaps = set()
        for r in self.validation_results:
            all_gaps.update(r["tool_gaps"])

        if all_gaps:
            print("\nCommon Tool Gaps (across all scenarios):")
            for gap in sorted(all_gaps):
                count = sum(1 for r in self.validation_results if gap in r["tool_gaps"])
                print(f"  • {gap} (needed by {count} scenarios)")

        # Component performance
        print("\nComponent Capability Assessment:")
        planner_ok = sum(1 for r in self.validation_results if r["planner_capability"][0])
        executor_ok = sum(1 for r in self.validation_results if r["executor_capability"][0])
        verifier_ok = sum(1 for r in self.validation_results if r["verifier_capability"][0])

        print(f"  Planner can handle: {planner_ok}/{total} scenarios ({planner_ok / total * 100:.0f}%)")
        print(f"  Executor can handle: {executor_ok}/{total} scenarios ({executor_ok / total * 100:.0f}%)")
        print(f"  Verifier can handle: {verifier_ok}/{total} scenarios ({verifier_ok / total * 100:.0f}%)")

        print(f"\n{'=' * 80}")
        print("RECOMMENDATION: MVP Architecture Assessment")
        print("=" * 80)

        if fully_supported >= 7:
            print("\n✓ STRONG MVP: Architecture supports 70%+ of scenarios")
            print("  → Proceed with implementation")
            print("  → Add missing tools iteratively in V1.0")
        elif fully_supported >= 5:
            print("\n⚠ ACCEPTABLE MVP: Architecture supports 50%+ of scenarios")
            print("  → Consider adding 1-2 critical tools before launch")
            print("  → Document known limitations clearly")
        else:
            print("\n✗ WEAK MVP: Architecture supports <50% of scenarios")
            print("  → Expand tool set before proceeding")
            print("  → Re-evaluate core architecture decisions")

    def _save_results(self):
        """Save validation results to JSON"""

        output_dir = Path(__file__).parent / "results"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "architecture_validation.json"

        with open(output_file, "w") as f:
            json.dump(
                {
                    "validation_type": "architecture_design",
                    "total_scenarios": len(self.validation_results),
                    "results": self.validation_results,
                },
                f,
                indent=2,
            )

        print(f"\n✓ Validation results saved to: {output_file}")


def main():
    """Run architecture validation"""
    validator = ArchitectureValidator()
    validator.run_all_scenarios()


if __name__ == "__main__":
    main()
