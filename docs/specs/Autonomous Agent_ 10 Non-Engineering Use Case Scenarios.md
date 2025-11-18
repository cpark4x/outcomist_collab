# Autonomous Agent: 10 Non-Engineering Use Case Scenarios

This document summarizes the 10 core use case scenarios developed to validate the robustness of the **Planner → Executor → Verifier (P→E→V)** architecture and the core value proposition of **Trusted Delegation** across the primary target user segment (Non-Engineers).

Each scenario demonstrates the Verifier Agent's ability to enforce a specific, non-trivial constraint.

| # | User Role | Core Task | Verifier's Key Role | Score |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Product Manager | Competitive Analysis Report & Deck | Enforcing **Structural** (10 slides) and **Factual** (data freshness) constraints. | 5/5 |
| **2** | Marketing Manager | Launch Email Campaign & CSV | Enforcing **Structural** (CSV format) and **Non-Destructive Action** (Drafts folder) constraints. | 5/5 |
| **3** | Financial Analyst | CAGR Calculation & Python Script | Enforcing **Factual** (financial correctness), **Structural** (code comments), and **Formatting** (Excel % decimals) constraints. | 5/5 |
| **4** | HR Manager | Remote Work Policy (PDF) | Enforcing **Factual** (legal compliance with AB 1234) and **Structural** (PDF format) constraints. | 5/5 |
| **5** | Sales Ops Manager | Personalized Motivational Emails | Enforcing **Factual** (correct revenue number) and **Non-Destructive Action** (Drafts folder) constraints. | 5/5 |
| **6** | Executive Assistant | Chronological Briefing Notes | Enforcing **Content** (3-sentence limit) and **Factual** (recent news) constraints. | 5/5 |
| **7** | Product Marketing | Facebook Ad Headlines (JSON) | Enforcing **Creative** (length < 40 chars) and **Content** (exact phrase 'Save 10 Hours') constraints. | 5/5 |
| **8** | Academic Researcher | APA Bibliography & Summary | Enforcing **Structural** (APA format) and **Factual** (correct summary of findings) constraints. | 5/5 |
| **9** | Small Business Owner | Responsive Landing Page | Enforcing **Functional** (correct Shopify link) and **Performance** (PageSpeed > 90) constraints. | 5/5 |
| **10** | Operations Manager | Workflow Automation Script | Enforcing **Functional** (correct Slack channel ID) and **Constraint** (Jira priority) constraints. | 5/5 |

---

## Detailed Scenario Breakdown

### Scenario 1: Product Manager (Competitive Analysis)

**Task:** Generate a competitive analysis report on Domino's and Papa John's, including a 10-slide summary deck. Use only data from the last 18 months.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the multi-artifact, multi-constraint task.
*   **Executor:** Runs research and content generation tools.
*   **Verifier's Key Action:** Checks the final deck for **exactly 10 slides** (Structural Constraint) and confirms all data sources used are within the **18-month freshness window** (Factual Constraint).
*   **Trust Moment:** The user trusts the final deck is ready for the executive meeting without having to count slides or check data timestamps.

### Scenario 2: Marketing Manager (Launch Email Campaign)

**Task:** Draft a launch email campaign (3 emails) for the new 'Velocity' feature. The final output must be in a single, ready-to-upload **.csv file**.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the creative task with a strict technical output format.
*   **Executor:** Runs creative writing and file formatting tools.
*   **Verifier's Key Action:** Checks the final output for **valid CSV structure** (Structural Constraint). If the Executor uses the wrong delimiter, the Verifier fails the output and forces a self-correction to fix the file format.
*   **Trust Moment:** The user trusts the file is ready for immediate upload to the marketing automation system without manual file inspection.

### Scenario 3: Financial Analyst (CAGR Calculation)

**Task:** Generate a **Python script** that calculates the Compound Annual Growth Rate (CAGR) for 3 competitors and output the results into a **single Excel spreadsheet** with the CAGR formatted as a percentage with two decimal places.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the complex, multi-artifact task involving code and data.
*   **Executor:** Runs code generation and data analysis tools.
*   **Verifier's Key Action:** Performs an **independent calculation** of the CAGR to verify the Executor's result (Factual Constraint). It also checks the Excel file for the **correct percentage formatting** (Formatting Constraint).
*   **Trust Moment:** The user trusts the financial data is arithmetically correct and ready for presentation.

### Scenario 4: HR Manager (Remote Work Policy)

**Task:** Draft a new 'Remote Work Policy' document based on the latest California labor laws (AB 1234).

**P→E→V Flow Summary:**
*   **Planner:** Interprets the high-stakes legal compliance task.
*   **Executor:** Runs deep research and policy drafting tools.
*   **Verifier's Key Action:** Checks the drafted policy against the **explicit text of AB 1234** (Factual/Legal Constraint). If a mandatory clause is missing, the Verifier forces the Planner to insert it.
*   **Trust Moment:** The user trusts the policy is compliant with external, non-negotiable legal requirements.

### Scenario 5: Sales Ops Manager (Personalized Motivational Emails)

**Task:** Identify the top 5 sales reps by revenue (from a CSV) and generate a personalized, motivational email for each, highlighting their specific revenue number and rank.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the data analysis and personalized communication task.
*   **Executor:** Runs data analysis and creative writing tools.
*   **Verifier's Key Action:** Checks the personalized email content against the source CSV to ensure the **revenue number and rank are factually correct** for each rep (Factual Constraint).
*   **Trust Moment:** The user trusts the personalized communication is accurate and will not embarrass the company with incorrect data.

### Scenario 6: Executive Assistant (Chronological Briefing Notes)

**Task:** Write a 3-sentence briefing note for each external meeting, summarizing their role and company's recent news.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the synthesis and content constraint task.
*   **Executor:** Runs research and writing tools.
*   **Verifier's Key Action:** Checks the length of each note to ensure it is **exactly 3 sentences** (Content Constraint). It also checks the news to ensure it is **recent** (Factual Constraint).
*   **Trust Moment:** The user trusts the briefing is concise and accurate for immediate use by the CEO.

### Scenario 7: Product Marketing Manager (Facebook Ad Headlines)

**Task:** Generate 10 unique ad headlines that contain the phrase 'Save 10 Hours' and are under 40 characters. Output the final list in a JSON file.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the creative task with strict technical and content rules.
*   **Executor:** Runs creative writing and file formatting tools.
*   **Verifier's Key Action:** Checks every headline for **character count** (Creative Constraint) and the **exact required phrase** (Content Constraint).
*   **Trust Moment:** The user trusts the output can be immediately uploaded to the ad platform without being rejected for length or content violations.

### Scenario 8: Academic Researcher (APA Bibliography)

**Task:** Summarize the key findings of the top 5 most-cited papers into a single, **APA-formatted** bibliography and summary document.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the complex research and strict formatting task.
*   **Executor:** Runs academic research and writing tools.
*   **Verifier's Key Action:** Checks the bibliography for **correct APA formatting** (Structural Constraint) and verifies the **accuracy of the summarized findings** (Factual Constraint).
*   **Trust Moment:** The user trusts the document meets the rigorous standards of academic publishing.

### Scenario 9: Small Business Owner (Responsive Landing Page)

**Task:** Generate a responsive landing page that links to Shopify and must pass the **Google PageSpeed Insights mobile test with a score of 90 or higher.**

**P→E→V Flow Summary:**
*   **Planner:** Interprets the functional and performance-based code task.
*   **Executor:** Runs web development and temporary deployment tools.
*   **Verifier's Key Action:** **Runs the Google PageSpeed Insights tool** on the temporary deployment to verify the score (Performance Constraint). It also checks the CTA link for the correct Shopify URL (Functional Constraint).
*   **Trust Moment:** The user trusts the delivered code is optimized and functional, meeting external performance benchmarks.

### Scenario 10: Operations Manager (Workflow Automation Script)

**Task:** Create a workflow automation script that monitors a Slack channel for 'URGENT,' creates a high-priority Jira ticket, and sends a confirmation message back to the correct Slack channel.

**P→E→V Flow Summary:**
*   **Planner:** Interprets the integrated workflow automation task.
*   **Executor:** Runs workflow generation and integration testing tools.
*   **Verifier's Key Action:** **Runs a live test** by posting the keyword to a test channel and verifies that the **Jira ticket is created** and the **confirmation message is sent to the correct channel ID** (Functional Constraint).
*   **Trust Moment:** The user trusts the automation is correctly configured and will not fail in a critical operational moment.
