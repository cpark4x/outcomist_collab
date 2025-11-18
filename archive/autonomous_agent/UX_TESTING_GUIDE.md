# UX Testing Guide - Autonomous Agent

## Quick Start: Test the Web App Yourself (5 Minutes)

### Prerequisites

1. **Backend running**: `http://localhost:8000`
2. **Frontend running**: `http://localhost:5173`
3. **API key set**: `export ANTHROPIC_API_KEY=your_key`

### Your First Test

**Open**: `http://localhost:5173`

**Try this simple task**:
```
Goal: "Generate 5 Facebook ad headlines for a productivity app.
Each headline must be under 40 characters and include the phrase 'Save Time'."
```

**What to observe**:
1. ✅ Form is clear and inviting
2. ✅ "Delegate Task" button feels right (not "Submit")
3. ✅ Redirects to progress view automatically
4. ✅ Three-stage pipeline shows current status
5. ✅ Results show artifacts with download buttons
6. ✅ Verification badge shows confidence %
7. ✅ Can click back to dashboard to see history

**Expected time**: ~30 seconds (depending on backend)

---

## Self-Testing Scenarios (Ready Today)

These 5 scenarios are fully supported by the MVP. Test each one:

### Scenario 1: Marketing Email Campaign ✅

**Navigate to**: Dashboard → "Delegate Task"

**Input**:
```
Goal: Draft a 3-email launch sequence for our new "Velocity" feature.
Output as a CSV file ready for upload to our email platform.

Context:
- Product: Velocity (workflow automation)
- Audience: Existing customers
- Emails: Announcement, Benefits, Call-to-Action

Constraints:
- Must be CSV format
- Include: subject, preview_text, body_html, send_delay_days
```

**What to test**:
- [ ] Task submission feels natural
- [ ] Progress updates show what's happening
- [ ] CSV artifact downloads correctly
- [ ] Can open CSV in Excel/Google Sheets
- [ ] Verification shows "Valid CSV structure"

**Success criteria**: You get a working CSV with 3 emails

---

### Scenario 2: Sales Rep Personalization ✅

**Input**:
```
Goal: Create personalized motivational emails for our top 5 sales reps.

Context:
- Use this sample data:
  Rep 1: Alice Johnson, $450,000 revenue
  Rep 2: Bob Smith, $420,000 revenue
  Rep 3: Carol Davis, $390,000 revenue
  Rep 4: David Wilson, $375,000 revenue
  Rep 5: Eva Martinez, $360,000 revenue

Constraints:
- Each email must mention their specific revenue and rank
- Tone: Professional but motivational
- Output as JSON
```

**What to test**:
- [ ] Planner breaks down the data analysis step
- [ ] Executor generates 5 distinct emails
- [ ] Verification checks revenue accuracy
- [ ] JSON downloads and parses correctly
- [ ] Each email feels personalized

**Success criteria**: 5 unique emails with correct revenue/ranking

---

### Scenario 3: Executive Briefing Notes ✅

**Input**:
```
Goal: Write 3-sentence briefing notes for my 3 upcoming meetings.

Context:
- Meeting 1: Jane Smith, CEO of Acme Corp
- Meeting 2: Bob Johnson, CTO of TechStart Inc
- Meeting 3: Alice Williams, VP Product at DataFlow Systems

Constraints:
- Exactly 3 sentences per briefing
- Include recent company news (last 30 days)
- Format as markdown
```

**What to test**:
- [ ] Research step finds recent news
- [ ] Each brief is exactly 3 sentences
- [ ] Verification counts sentences correctly
- [ ] Markdown is readable
- [ ] News is actually recent

**Success criteria**: 3 concise, informative briefs

---

### Scenario 4: Facebook Ad Headlines ✅

**Input**:
```
Goal: Generate 10 Facebook ad headlines for our productivity tool.

Constraints:
- Each headline must be under 40 characters
- Each must include the phrase "Save 10 Hours"
- All must be unique
- Output as JSON
```

**What to test**:
- [ ] All headlines under 40 chars
- [ ] All include "Save 10 Hours"
- [ ] Verification checks character count
- [ ] Verification checks required phrase
- [ ] Headlines are creative and varied

**Success criteria**: 10 compliant, creative headlines

---

### Scenario 5: Academic Bibliography ✅

**Input**:
```
Goal: Create an APA-formatted bibliography of the top 5 papers on
"machine learning interpretability" with a 2-sentence summary of each.

Constraints:
- APA 7th edition format
- Include DOIs if available
- Summarize key findings
- Output as markdown
```

**What to test**:
- [ ] Research finds relevant papers
- [ ] APA formatting looks correct
- [ ] Summaries are clear and accurate
- [ ] Verification checks format
- [ ] Download works

**Success criteria**: Professional bibliography ready for use

---

## UX Evaluation Checklist

### 1. First Impressions (0-10 seconds)

When you land on the dashboard:

- [ ] **Clear purpose**: Do you immediately understand what this does?
- [ ] **Inviting**: Does the "Delegate Task" CTA draw you in?
- [ ] **Professional**: Does it look trustworthy?
- [ ] **Not chat**: Is it clear this ISN'T a chat interface?

**Rate (1-5)**: ___

**Notes**:
```
What works:

What's confusing:

```

---

### 2. Task Submission Experience

When filling out the task form:

- [ ] **Textarea feels right**: Is it big enough for detailed goals?
- [ ] **Placeholder helpful**: Does example text guide you?
- [ ] **Optional fields clear**: Do you understand Context/Constraints?
- [ ] **Button copy right**: Does "Delegate Task" feel better than "Submit"?
- [ ] **Validation helpful**: Do error messages guide you?

**Rate (1-5)**: ___

**Notes**:
```
What works:

What needs improvement:

```

---

### 3. Progress Monitoring

While task is running:

- [ ] **Pipeline visible**: Can you see Planning → Executing → Verifying?
- [ ] **Current activity clear**: Do you know what's happening now?
- [ ] **Time visible**: Can you see elapsed time?
- [ ] **Not anxious**: Do you feel informed, not worried?
- [ ] **Real-time updates**: Does the page refresh appropriately?

**Rate (1-5)**: ___

**Notes**:
```
What works:

What causes anxiety:

```

---

### 4. Results & Trust

When task completes:

- [ ] **Artifacts obvious**: Can you immediately find what you need?
- [ ] **Download easy**: Is it one click to get the file?
- [ ] **Verification visible**: Do you see the quality badge?
- [ ] **Confidence clear**: Is the percentage meaningful?
- [ ] **Checks detailed**: Can you see what was verified?
- [ ] **Issues addressed**: If there are issues, are they clear?

**Rate (1-5)**: ___

**Trust Question**: Would you use this artifact without reviewing it?
- [ ] Yes, completely
- [ ] Yes, with quick scan
- [ ] No, need full review
- [ ] No, don't trust it

**Notes**:
```
What builds trust:

What undermines trust:

```

---

### 5. Navigation & History

Using the dashboard:

- [ ] **History accessible**: Easy to find past tasks?
- [ ] **Filtering works**: Can you filter by status?
- [ ] **Task cards informative**: Can you tell tasks apart?
- [ ] **Click through natural**: Easy to view details?
- [ ] **Back button works**: Can you navigate back?

**Rate (1-5)**: ___

**Notes**:
```
What works:

What's clunky:

```

---

### 6. Mobile Experience (Optional)

Open on phone (`http://localhost:5173` or deployed URL):

- [ ] **Responsive layout**: Does it adapt to small screen?
- [ ] **Touch targets**: Can you tap buttons easily?
- [ ] **Text readable**: Is font size appropriate?
- [ ] **Forms usable**: Can you type in textarea?
- [ ] **Overall functional**: Would you use this on mobile?

**Rate (1-5)**: ___

---

## Comparative Analysis

### vs. ChatGPT/Claude

What's **better** about this experience:
```
1.
2.
3.
```

What's **worse**:
```
1.
2.
3.
```

What's **different** (neutral):
```
1.
2.
3.
```

---

### vs. Traditional Forms

What's **better** about this vs. filling out a form:
```
1.
2.
3.
```

What's **worse**:
```
1.
2.
3.
```

---

## Key UX Questions

### Delegation Paradigm

**Q**: Does this feel like delegation (assigning work) or assistance (getting help)?
```
Answer:

Evidence:
```

**Q**: Do you feel like the "manager" of this agent, or like a "user" of a tool?
```
Answer:

Why:
```

---

### Trust Building

**Q**: At what point do you start trusting the output?
- [ ] Immediately when it completes
- [ ] After seeing verification badge
- [ ] After reviewing the artifact
- [ ] After using it successfully once
- [ ] Never fully trust it

**Q**: What would increase your trust?
```
1.
2.
3.
```

---

### Verification Transparency

**Q**: Is the verification visible enough?
- [ ] Too prominent (in the way)
- [ ] Just right (noticeable but not intrusive)
- [ ] Too subtle (easy to miss)
- [ ] Not visible enough

**Q**: Does the confidence percentage feel meaningful?
```
Answer:

Why/why not:
```

---

### Task Completion Feeling

**Q**: When the task completes, how do you feel?
- [ ] Relieved (it's done!)
- [ ] Suspicious (is it really right?)
- [ ] Curious (let me check)
- [ ] Confident (ready to use)
- [ ] Other: ___________

**Q**: What would make you feel more confident?
```
1.
2.
3.
```

---

## Issues Log

Track any bugs, glitches, or confusing moments:

| Time | Issue | Severity | Expected Behavior | Actual Behavior |
|------|-------|----------|-------------------|-----------------|
| | | High/Med/Low | | |
| | | | | |
| | | | | |

---

## Observed Pain Points

### Critical (Blocks usage)
```
1.
2.
3.
```

### Major (Frustrating but usable)
```
1.
2.
3.
```

### Minor (Annoying but ignorable)
```
1.
2.
3.
```

---

## Suggestions for Improvement

### Must Have (Before Launch)
```
1.
2.
3.
```

### Should Have (V1.0)
```
1.
2.
3.
```

### Nice to Have (Future)
```
1.
2.
3.
```

---

## Overall Assessment

### Would you use this?
- [ ] Yes, regularly
- [ ] Yes, occasionally
- [ ] Maybe, depends on use case
- [ ] Probably not
- [ ] Definitely not

**Why/why not**:
```


```

### Would you recommend this to a colleague?
- [ ] Yes, enthusiastically
- [ ] Yes, with caveats
- [ ] Neutral
- [ ] Probably not
- [ ] No

**What would you tell them**:
```


```

---

## Next Steps After Self-Testing

### 1. Fix Critical Issues
Document any blocking issues and prioritize fixes.

### 2. Recruit Real Users
Once you're confident, recruit 5 users (1 per supported scenario):
- Marketing Manager
- Sales Ops Manager
- Executive Assistant
- Product Marketing Manager
- Academic Researcher

### 3. Structured User Testing
Give them the scenarios above and watch them use it (don't help!).

### 4. Post-Task Interviews
Ask them:
- "Would you trust this output without reviewing it?"
- "What would increase your confidence?"
- "How does this compare to ChatGPT/Claude?"
- "What would make you use this regularly?"

### 5. Iterate
Based on feedback, prioritize UX improvements for V1.0.

---

## Testing Tools (Optional)

### Screen Recording
Record your session to review later:
- Mac: QuickTime (built-in)
- Windows: Xbox Game Bar (built-in)
- Chrome: Loom extension

### Analytics (Future)
Consider adding:
- Task completion time
- Verification acceptance rate
- Artifact download rate
- Retry rate
- Error rate

---

## Success Metrics

After testing, you should be able to answer:

✅ **Usability**: Can users complete tasks without help?
✅ **Trust**: Do users trust the output enough to use it?
✅ **Speed**: Is task completion fast enough?
✅ **Clarity**: Do users understand the verification?
✅ **Value**: Would users pay for this?

If yes to 4/5 → Ready to launch
If yes to 3/5 → Fix critical issues first
If yes to <3/5 → Major UX revision needed

---

## Quick Test Script (5 Minutes)

If you only have 5 minutes, do this:

**Minute 1**: Open dashboard, read it, first impression?
**Minute 2**: Submit the Facebook ad headline task
**Minute 3**: Watch progress pipeline update
**Minute 4**: Review results and verification
**Minute 5**: Download artifact and check quality

**One question**: Would you use this artifact without reviewing it?

If **YES** → Your UX is working
If **NO** → Document why and fix before launch

---

*Save this completed guide as `UX_TESTING_RESULTS_[DATE].md`*
