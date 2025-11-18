"""
Test suite for 10 Non-Engineering Use Case Scenarios

This validates the P→E→V architecture against real-world delegation tasks
from Product Managers, Marketing Managers, Financial Analysts, etc.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.executor import ExecutorAgent
from src.agents.planner import PlannerAgent
from src.agents.verifier import VerifierAgent
from src.core.contracts import TaskIntent
from src.core.orchestrator import Orchestrator


class ScenarioTester:
    """Test runner for non-engineering use case scenarios"""

    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set. Please set it to run scenario tests.")

        self.orchestrator = Orchestrator(
            planner=PlannerAgent(api_key=api_key),
            executor=ExecutorAgent(api_key=api_key),
            verifier=VerifierAgent(api_key=api_key),
        )
        self.results: List[Dict[str, Any]] = []

    async def run_scenario(
        self,
        scenario_num: int,
        user_role: str,
        goal: str,
        context: Dict[str, Any],
        constraints: Dict[str, Any],
        expected_artifacts: List[str],
        verifier_key_checks: List[str],
    ) -> Dict[str, Any]:
        """Run a single scenario and capture results"""

        print(f"\n{'=' * 80}")
        print(f"SCENARIO {scenario_num}: {user_role}")
        print(f"{'=' * 80}")
        print(f"Goal: {goal}")
        print(f"Constraints: {json.dumps(constraints, indent=2)}")
        print()

        # Create task intent
        intent = TaskIntent(
            goal=goal, context=context, constraints=constraints, user_id=f"test_scenario_{scenario_num}"
        )

        # Execute task
        start_time = datetime.now()
        try:
            result = await self.orchestrator.execute_task(intent)
            execution_time = (datetime.now() - start_time).total_seconds()

            # Evaluate results
            evaluation = {
                "scenario_num": scenario_num,
                "user_role": user_role,
                "success": result.success,
                "execution_time": execution_time,
                "artifacts_generated": len(result.artifacts),
                "expected_artifacts": len(expected_artifacts),
                "artifacts_match": len(result.artifacts) >= len(expected_artifacts),
                "validation_passed": result.validation.passed,
                "validation_confidence": result.validation.confidence,
                "verifier_checks_run": len(result.validation.checks),
                "expected_verifier_checks": len(verifier_key_checks),
                "issues_found": len(result.validation.issues),
                "artifacts": [
                    {"type": a.artifact_type, "name": a.name, "content_size": len(str(a.content))}
                    for a in result.artifacts
                ],
                "validation_details": {
                    "checks": [
                        {"name": c.name, "passed": c.passed, "message": c.message} for c in result.validation.checks
                    ],
                    "issues": [
                        {"severity": i.severity, "message": i.message, "location": i.location}
                        for i in result.validation.issues
                    ],
                },
            }

            # Print summary
            print(f"✓ Task completed in {execution_time:.1f}s")
            print(f"  Artifacts: {len(result.artifacts)}/{len(expected_artifacts)} expected")
            print(
                f"  Validation: {'PASSED' if result.validation.passed else 'FAILED'} "
                f"({result.validation.confidence:.1%} confidence)"
            )
            print(f"  Verifier checks: {len(result.validation.checks)}")
            print(f"  Issues found: {len(result.validation.issues)}")

            if not result.validation.passed:
                print("\n  Issues:")
                for issue in result.validation.issues:
                    print(f"    [{issue.severity}] {issue.message}")

            self.results.append(evaluation)
            return evaluation

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            evaluation = {
                "scenario_num": scenario_num,
                "user_role": user_role,
                "success": False,
                "execution_time": execution_time,
                "error": str(e),
                "error_type": type(e).__name__,
            }
            print(f"✗ Task failed after {execution_time:.1f}s: {e}")
            self.results.append(evaluation)
            return evaluation

    async def run_all_scenarios(self):
        """Run all 10 non-engineering use case scenarios"""

        scenarios = [
            # Scenario 1: Product Manager - Competitive Analysis
            {
                "scenario_num": 1,
                "user_role": "Product Manager",
                "goal": "Generate a competitive analysis report on Domino's and Papa John's pizza chains, including a 10-slide summary deck. Use only data from the last 18 months.",
                "context": {
                    "competitors": ["Domino's", "Papa John's"],
                    "analysis_areas": ["market share", "pricing", "technology", "customer satisfaction"],
                    "time_period": "last 18 months",
                },
                "constraints": {
                    "deck_slides": 10,
                    "data_freshness": "18 months maximum",
                    "output_formats": ["PDF report", "PPTX deck"],
                },
                "expected_artifacts": ["competitive_analysis.pdf", "summary_deck.pptx"],
                "verifier_key_checks": [
                    "Exactly 10 slides in deck",
                    "All data sources within 18-month window",
                    "Both competitors analyzed",
                ],
            },
            # Scenario 2: Marketing Manager - Launch Email Campaign
            {
                "scenario_num": 2,
                "user_role": "Marketing Manager",
                "goal": "Draft a launch email campaign (3 emails) for the new 'Velocity' feature. The final output must be in a single, ready-to-upload CSV file with proper email marketing format.",
                "context": {
                    "product": "Velocity feature",
                    "email_sequence": ["announcement", "benefits", "call_to_action"],
                    "target_audience": "existing customers",
                },
                "constraints": {
                    "email_count": 3,
                    "output_format": "CSV",
                    "csv_columns": ["subject", "preview_text", "body_html", "send_delay_days"],
                },
                "expected_artifacts": ["email_campaign.csv"],
                "verifier_key_checks": ["Valid CSV structure", "3 email rows present", "All required columns present"],
            },
            # Scenario 3: Financial Analyst - CAGR Calculation
            {
                "scenario_num": 3,
                "user_role": "Financial Analyst",
                "goal": "Generate a Python script that calculates the Compound Annual Growth Rate (CAGR) for 3 competitors and output the results into a single Excel spreadsheet with the CAGR formatted as a percentage with two decimal places.",
                "context": {
                    "competitors": ["Company A", "Company B", "Company C"],
                    "revenue_data": {
                        "Company A": {"2020": 1000000, "2024": 1500000},
                        "Company B": {"2020": 800000, "2024": 1200000},
                        "Company C": {"2020": 1200000, "2024": 1800000},
                    },
                },
                "constraints": {
                    "output_format": "Excel (.xlsx)",
                    "cagr_format": "percentage with 2 decimals",
                    "include_python_script": True,
                },
                "expected_artifacts": ["cagr_calculator.py", "cagr_results.xlsx"],
                "verifier_key_checks": [
                    "CAGR calculations mathematically correct",
                    "Excel formatting matches specification",
                    "Python script is executable",
                ],
            },
            # Scenario 4: HR Manager - Remote Work Policy
            {
                "scenario_num": 4,
                "user_role": "HR Manager",
                "goal": "Draft a new 'Remote Work Policy' document based on the latest California labor laws (AB 1234). Output as PDF.",
                "context": {
                    "jurisdiction": "California",
                    "relevant_law": "AB 1234",
                    "company_size": "50-200 employees",
                    "industry": "Technology",
                },
                "constraints": {
                    "compliance_requirements": ["AB 1234 mandatory clauses"],
                    "output_format": "PDF",
                    "must_include": ["work hours", "equipment", "expense reimbursement", "privacy"],
                },
                "expected_artifacts": ["remote_work_policy.pdf"],
                "verifier_key_checks": [
                    "AB 1234 compliance verified",
                    "All mandatory sections present",
                    "PDF format valid",
                ],
            },
            # Scenario 5: Sales Ops Manager - Personalized Motivational Emails
            {
                "scenario_num": 5,
                "user_role": "Sales Ops Manager",
                "goal": "Identify the top 5 sales reps by revenue from the provided CSV and generate a personalized, motivational email for each, highlighting their specific revenue number and rank.",
                "context": {
                    "sales_data_csv": "sales_q4_2024.csv",
                    "email_tone": "motivational and professional",
                    "include_metrics": True,
                },
                "constraints": {
                    "top_count": 5,
                    "personalization_required": ["name", "revenue", "rank"],
                    "revenue_accuracy": "must match CSV exactly",
                },
                "expected_artifacts": ["rep_emails.json"],
                "verifier_key_checks": [
                    "Revenue numbers match source CSV",
                    "Correct ranking (1-5)",
                    "All 5 emails personalized",
                ],
            },
            # Scenario 6: Executive Assistant - Chronological Briefing Notes
            {
                "scenario_num": 6,
                "user_role": "Executive Assistant",
                "goal": "Write a 3-sentence briefing note for each of 5 external meetings, summarizing the attendee's role and their company's recent news.",
                "context": {
                    "meetings": [
                        {"company": "Acme Corp", "attendee": "Jane Smith, CEO"},
                        {"company": "TechStart Inc", "attendee": "Bob Johnson, CTO"},
                        {"company": "DataFlow Systems", "attendee": "Alice Williams, VP Product"},
                        {"company": "CloudScale", "attendee": "Mike Davis, Head of Sales"},
                        {"company": "AI Innovations", "attendee": "Sarah Chen, Founder"},
                    ]
                },
                "constraints": {
                    "sentences_per_note": 3,
                    "news_recency": "last 30 days",
                    "format": "concise bullet points",
                },
                "expected_artifacts": ["meeting_briefs.md"],
                "verifier_key_checks": [
                    "Exactly 3 sentences per brief",
                    "Recent news included",
                    "All 5 meetings covered",
                ],
            },
            # Scenario 7: Product Marketing - Facebook Ad Headlines
            {
                "scenario_num": 7,
                "user_role": "Product Marketing Manager",
                "goal": "Generate 10 unique Facebook ad headlines that contain the phrase 'Save 10 Hours' and are under 40 characters. Output the final list in a JSON file.",
                "context": {
                    "product": "Productivity automation tool",
                    "target_audience": "busy professionals",
                    "campaign_theme": "time savings",
                },
                "constraints": {
                    "headline_count": 10,
                    "required_phrase": "Save 10 Hours",
                    "max_characters": 40,
                    "output_format": "JSON",
                },
                "expected_artifacts": ["ad_headlines.json"],
                "verifier_key_checks": [
                    "All headlines under 40 characters",
                    "All headlines contain 'Save 10 Hours'",
                    "Exactly 10 unique headlines",
                ],
            },
            # Scenario 8: Academic Researcher - APA Bibliography
            {
                "scenario_num": 8,
                "user_role": "Academic Researcher",
                "goal": "Summarize the key findings of the top 5 most-cited papers on 'machine learning interpretability' into a single, APA-formatted bibliography and summary document.",
                "context": {
                    "research_topic": "machine learning interpretability",
                    "paper_count": 5,
                    "citation_threshold": "top cited papers",
                },
                "constraints": {
                    "citation_format": "APA 7th edition",
                    "output_format": "PDF",
                    "include_summaries": True,
                },
                "expected_artifacts": ["ml_interpretability_bibliography.pdf"],
                "verifier_key_checks": [
                    "APA formatting correct",
                    "5 papers included",
                    "Key findings summarized accurately",
                ],
            },
            # Scenario 9: Small Business Owner - Responsive Landing Page
            {
                "scenario_num": 9,
                "user_role": "Small Business Owner",
                "goal": "Generate a responsive landing page that links to my Shopify store and must pass the Google PageSpeed Insights mobile test with a score of 90 or higher.",
                "context": {
                    "shopify_url": "https://mystore.myshopify.com",
                    "business_type": "e-commerce",
                    "primary_cta": "Shop Now",
                },
                "constraints": {
                    "responsive_design": True,
                    "pagespeed_mobile_score": 90,
                    "shopify_link_functional": True,
                },
                "expected_artifacts": ["landing_page.html", "styles.css"],
                "verifier_key_checks": ["PageSpeed score >= 90", "Shopify URL correct", "Mobile responsive verified"],
            },
            # Scenario 10: Operations Manager - Workflow Automation Script
            {
                "scenario_num": 10,
                "user_role": "Operations Manager",
                "goal": "Create a workflow automation script that monitors a Slack channel for the keyword 'URGENT', creates a high-priority Jira ticket, and sends a confirmation message back to the correct Slack channel.",
                "context": {"slack_channel": "#ops-alerts", "jira_project": "OPS", "trigger_keyword": "URGENT"},
                "constraints": {
                    "jira_priority": "High",
                    "slack_confirmation": True,
                    "test_mode": True,  # MVP: Mock the integrations
                },
                "expected_artifacts": ["workflow_automation.py"],
                "verifier_key_checks": [
                    "Jira ticket created with High priority",
                    "Slack confirmation sent to correct channel",
                    "Keyword detection works",
                ],
            },
        ]

        print("\n" + "=" * 80)
        print("AUTONOMOUS AGENT - 10 NON-ENGINEERING USE CASE SCENARIOS")
        print("Testing P→E→V Architecture Against Real-World Delegation Tasks")
        print("=" * 80)

        for scenario in scenarios:
            await self.run_scenario(**scenario)
            await asyncio.sleep(1)  # Brief pause between scenarios

        self._print_summary()
        self._save_results()

    def _print_summary(self):
        """Print summary statistics across all scenarios"""

        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)

        total = len(self.results)
        successful = sum(1 for r in self.results if r.get("success", False))
        validated = sum(1 for r in self.results if r.get("validation_passed", False))

        total_time = sum(r.get("execution_time", 0) for r in self.results)
        avg_time = total_time / total if total > 0 else 0
        avg_confidence = sum(r.get("validation_confidence", 0) for r in self.results) / total if total > 0 else 0

        print("\nExecution Summary:")
        print(f"  Total scenarios: {total}")
        print(f"  Successful executions: {successful}/{total} ({successful / total * 100:.1f}%)")
        print(f"  Validation passed: {validated}/{total} ({validated / total * 100:.1f}%)")
        print(f"  Total execution time: {total_time:.1f}s")
        print(f"  Average execution time: {avg_time:.1f}s")
        print(f"  Average validation confidence: {avg_confidence:.1%}")

        print("\nPer-Role Breakdown:")
        roles = {}
        for r in self.results:
            role = r.get("user_role", "Unknown")
            if role not in roles:
                roles[role] = {"total": 0, "success": 0, "validated": 0}
            roles[role]["total"] += 1
            if r.get("success", False):
                roles[role]["success"] += 1
            if r.get("validation_passed", False):
                roles[role]["validated"] += 1

        for role, stats in sorted(roles.items()):
            print(f"  {role}:")
            print(f"    Success: {stats['success']}/{stats['total']}")
            print(f"    Validated: {stats['validated']}/{stats['total']}")

        print("\nVerifier Performance:")
        for r in self.results:
            scenario = r.get("scenario_num", "?")
            checks = r.get("verifier_checks_run", 0)
            issues = r.get("issues_found", 0)
            confidence = r.get("validation_confidence", 0)
            print(f"  Scenario {scenario}: {checks} checks, {issues} issues, {confidence:.1%} confidence")

    def _save_results(self):
        """Save detailed results to JSON file"""

        output_dir = Path(__file__).parent / "results"
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"scenario_test_results_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(
                {"test_run": timestamp, "total_scenarios": len(self.results), "results": self.results}, f, indent=2
            )

        print(f"\n✓ Detailed results saved to: {output_file}")


async def main():
    """Run all scenario tests"""
    tester = ScenarioTester()
    await tester.run_all_scenarios()


if __name__ == "__main__":
    asyncio.run(main())
