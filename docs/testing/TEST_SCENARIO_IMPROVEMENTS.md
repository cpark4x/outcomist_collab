# Test Scenario Improvements - Objective Analysis

**Purpose**: Critical gaps and recommendations for E2E test execution
**Audience**: AI agent preparing to execute tests
**Date**: 2025-11-19

---

## Executive Summary

The USER_SCENARIOS.md document provides good narrative descriptions but **lacks execution specificity**. For an AI agent to run E2E tests successfully, it needs:

1. **Exact API endpoints and commands** to execute
2. **Concrete success/failure criteria** (not subjective descriptions)
3. **Observable checkpoints** at each step
4. **Failure mode injection methods** (how to create broken states)
5. **Rollback procedures** between tests
6. **Measurement instrumentation** (what to log, where)

---

## Critical Gaps Analysis

### Gap 1: Missing Execution Prerequisites

**Current State**: "Expected Experience: Outcomist shows progress..."

**Problem**: No specification of:
- How to start a test (API endpoint? UI automation? Direct service call?)
- Where to observe progress (UI polling? SSE stream? Database query?)
- What constitutes "shows progress" (specific log line? UI element? Status code?)

**Impact**: Agent cannot execute test without reverse-engineering system

---

### Gap 2: Vague Success Criteria

**Current State**:
```
Success Metrics:
- Game works on first try: ✅/❌
- Progress visible throughout: ✅/❌
```

**Problem**: "Works" and "visible" are subjective
- What does "game works" mean? No JS errors? Specific function returns value? User can click button?
- What does "visible" mean? Element exists in DOM? Text content updated? SSE event received?

**Impact**: Agent cannot determine pass/fail without human judgment

---

### Gap 3: No Failure Mode Injection

**Current State**: Tests assume natural system behavior (both success and failure)

**Problem**: E2E testing requires **controlled failure injection** to validate error handling:
- How to force a JavaScript error in generated game?
- How to simulate network timeout during build?
- How to create intentionally broken code?

**Impact**: Cannot test error recovery paths systematically

---

### Gap 4: Missing State Reset Procedures

**Current State**: No guidance on test isolation

**Problem**: Tests assume clean state but don't specify:
- How to reset database between tests?
- How to clear project directories?
- How to ensure no leftover SSE connections?
- How to reset session state?

**Impact**: Test pollution - failures cascade across tests

---

### Gap 5: No Observable Checkpoints

**Current State**: "Expected Experience: 1. Outcomist shows progress... 2. Progress steps visible..."

**Problem**: Steps are narrative, not measurable
- What specific log line confirms step 1 completion?
- What database field value indicates step 2?
- What HTTP response code means step 3 succeeded?

**Impact**: Cannot automate verification - requires manual observation

---

### Gap 6: Ambiguous Timing Expectations

**Current State**: "Takes ~5 minutes", "Quick update (< 1 minute)"

**Problem**: No failure thresholds
- If Charlotte's game takes 3.5 minutes instead of 3, is that a failure?
- What's the timeout before declaring test failed?
- What's acceptable variance?

**Impact**: Cannot determine if performance is acceptable

---

### Gap 7: Missing Log Capture Specification

**Current State**: Success metrics reference behavior, not artifacts

**Problem**: No specification of:
- Which log files to capture?
- What log levels matter? (INFO, DEBUG, ERROR)
- What keywords indicate success/failure?
- Where logs are stored?

**Impact**: Cannot collect evidence for test results

---

### Gap 8: No Playwright/Browser Automation Details

**Current State**: "Charlotte starts playing" or "Mason tests"

**Problem**: If using browser automation:
- What selectors identify UI elements?
- What JavaScript to execute in browser console?
- How to verify "game is playable"? (click event fires? canvas draws?)

**Impact**: Cannot automate UI testing

---

### Gap 9: Insufficient Failure Taxonomy

**Current State**: Single "✅/❌" per metric

**Problem**: Failures have types:
- **System failure**: Backend crashed
- **Verification failure**: Game has bugs but system working
- **Performance failure**: Took too long but works
- **UX failure**: Works but confusing to user
- **Data failure**: Wrong value in database

**Impact**: Cannot diagnose root cause from test results

---

### Gap 10: No Test Data Management

**Current State**: Tests reference "Charlotte's Tetris game" but don't specify:

**Problem**:
- What exact prompt text to use?
- What project name to create?
- What user ID to use?
- Where test artifacts are stored?

**Impact**: Tests not reproducible - different results each run

---

## Recommended Improvements

### Improvement 1: Add "Test Setup" Section

**For each scenario, add:**

```markdown
#### Test Setup - Charlotte Tetris (Scenario C1)

**Prerequisites**:
- Backend running on http://localhost:8000
- Frontend running on http://localhost:5173
- Database clean (no projects with name "charlotte-tetris-test")
- Log level: DEBUG
- Monitor file: `/tmp/outcomist_test_c1.log`

**Test Data**:
- Project name: `charlotte-tetris-test-{timestamp}`
- User ID: `test-user-charlotte`
- Exact prompt: "I want to make a Tetris game where I can play with colorful blocks"

**Setup Commands**:
```bash
# Reset database
sqlite3 outcomist.db "DELETE FROM projects WHERE name LIKE 'charlotte-tetris-test%';"

# Clear project directory
rm -rf data/projects/charlotte-tetris-test-*

# Start log capture
tail -f backend.log > /tmp/outcomist_test_c1.log &
LOG_PID=$!
```

**Teardown Commands**:
```bash
# Stop log capture
kill $LOG_PID

# Archive test artifacts
tar czf results/c1-$(date +%s).tar.gz /tmp/outcomist_test_c1.log data/projects/charlotte-tetris-test-*
```
```

---

### Improvement 2: Add Observable Checkpoints

**For each step, specify measurable checkpoint:**

```markdown
#### Execution Steps - Charlotte Tetris (Scenario C1)

**Step 1: Submit Request**

*Action*:
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"charlotte-tetris-test-123", "user_id":"test-user-charlotte", "prompt":"I want to make a Tetris game where I can play with colorful blocks"}'
```

*Observable Checkpoint*:
- HTTP Status: `201 Created`
- Response body contains: `"project_id": "<uuid>"`
- Database state: `SELECT status FROM projects WHERE name='charlotte-tetris-test-123'` returns `"PLANNING"`

*Failure Detection*:
- HTTP Status: `500` → System failure
- Response missing `project_id` → API contract broken
- Database status not "PLANNING" → State machine error

---

**Step 2: Monitor Progress**

*Action*:
```bash
# Open SSE stream
curl -N http://localhost:8000/api/projects/{project_id}/stream
```

*Observable Checkpoints*:
```
T+0s:   SSE event: {"type":"status_update", "status":"PLANNING", "message":"Creating your Tetris game..."}
T+5s:   SSE event: {"type":"progress", "step":"1/5", "message":"Building game board"}
T+10s:  SSE event: {"type":"progress", "step":"2/5", "message":"Adding colorful blocks"}
T+120s: SSE event: {"type":"status_update", "status":"WORKING"}
T+180s: SSE event: {"type":"status_update", "status":"COMPLETE"}
```

*Failure Detection*:
- No SSE events within 5s → Connection failed
- Status never reaches "COMPLETE" within 300s → Timeout
- SSE event contains `"error"` field → Build error
- Console errors in backend log → Internal failure

---

**Step 3: Verify Game File Created**

*Action*:
```bash
# Check file exists
ls -lh data/projects/charlotte-tetris-test-123/game.html

# Check file size reasonable
FILE_SIZE=$(stat -f%z data/projects/charlotte-tetris-test-123/game.html)
if [ $FILE_SIZE -lt 1000 ]; then
  echo "FAIL: File too small (likely empty or error page)"
  exit 1
fi
```

*Observable Checkpoint*:
- File exists: `data/projects/{project_id}/game.html`
- File size: > 1KB (not empty stub)
- File contains: `<canvas` or `<button` (interactive element)
- File does NOT contain: `onerror=`, `throw new Error`, `undefined()` (error patterns)

*Failure Detection*:
- File missing → Generation failed
- File < 1KB → Incomplete generation
- File contains error patterns → Broken code generated
```

---

### Improvement 3: Add Concrete Success Criteria

**Replace subjective metrics with measurable ones:**

```markdown
#### Success Criteria - Charlotte Tetris (Scenario C1)

**Metric 1: Game Works on First Try**

❌ **Current** (subjective):
- Game works on first try: ✅/❌

✅ **Improved** (measurable):
- [ ] File `game.html` exists and size > 1KB
- [ ] File contains interactive element: `<canvas` OR `<button` OR `<input`
- [ ] File does NOT contain error patterns:
  - `undefined is not a function`
  - `Cannot read property`
  - `ReferenceError`
  - `onerror=`
- [ ] Browser console shows 0 errors when loading file
- [ ] Keyboard event listeners registered (check via: `getEventListeners(window)` in devtools)

**Test Command**:
```bash
# Open in headless browser and check console
npx playwright test --headed <<EOF
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();

// Capture console errors
const errors = [];
page.on('console', msg => {
  if (msg.type() === 'error') errors.push(msg.text());
});

// Load game
await page.goto('file://$(pwd)/data/projects/charlotte-tetris-test-123/game.html');
await page.waitForTimeout(2000); // Let JS execute

// Check for errors
if (errors.length > 0) {
  console.log('FAIL: Console errors:', errors);
  process.exit(1);
}

// Check for interactive elements
const hasCanvas = await page.locator('canvas').count() > 0;
const hasButton = await page.locator('button').count() > 0;
if (!hasCanvas && !hasButton) {
  console.log('FAIL: No interactive elements found');
  process.exit(1);
}

console.log('PASS: Game works');
browser.close();
EOF
```

---

**Metric 2: Progress Visible Throughout**

❌ **Current** (subjective):
- Progress visible throughout: ✅/❌

✅ **Improved** (measurable):
- [ ] SSE stream delivers events every 5-30 seconds (no gaps > 30s)
- [ ] At least 3 progress events received before completion
- [ ] Each progress event has format: `{"type":"progress", "step":"X/Y", "message":"..."}`
- [ ] Progress steps sequential (1/5, 2/5, 3/5, not jumps)
- [ ] UI updates within 100ms of SSE event (measure via timestamp comparison)

**Test Command**:
```bash
# Capture SSE events with timestamps
curl -N http://localhost:8000/api/projects/{project_id}/stream | while IFS= read -r line; do
  echo "$(date +%s.%N): $line" >> /tmp/sse_events.log
done &

# After test completes, analyze
python3 <<EOF
import json
from datetime import datetime

with open('/tmp/sse_events.log') as f:
    events = [line.strip().split(': ', 1) for line in f]

# Check frequency
timestamps = [float(t) for t, _ in events]
gaps = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
if max(gaps) > 30:
    print(f'FAIL: Progress gap too long: {max(gaps)}s')
    exit(1)

# Check progress events
progress_events = [json.loads(data) for _, data in events if '"type":"progress"' in data]
if len(progress_events) < 3:
    print(f'FAIL: Only {len(progress_events)} progress events (expected >= 3)')
    exit(1)

print('PASS: Progress visible throughout')
EOF
```

---

**Metric 3: Time Estimate Accurate**

❌ **Current** (vague):
- Time estimate accurate (within 30 seconds): ✅/❌

✅ **Improved** (measurable):
- [ ] First SSE event includes `"estimated_time"` field in seconds
- [ ] Actual completion time within 30s of estimate (15% variance allowed)
- [ ] If estimate exceeded, progress events show updated estimates
- [ ] Final event includes `"actual_duration"` for comparison

**Test Command**:
```bash
# Extract timing from SSE events
START_TIME=$(grep '"status":"PLANNING"' /tmp/sse_events.log | head -1 | cut -d: -f1)
END_TIME=$(grep '"status":"COMPLETE"' /tmp/sse_events.log | head -1 | cut -d: -f1)
ESTIMATE=$(grep '"estimated_time"' /tmp/sse_events.log | head -1 | jq -r '.estimated_time')

ACTUAL_DURATION=$(echo "$END_TIME - $START_TIME" | bc)
DIFFERENCE=$(echo "$ACTUAL_DURATION - $ESTIMATE" | bc | tr -d '-')

if (( $(echo "$DIFFERENCE > 30" | bc -l) )); then
  echo "FAIL: Time estimate off by ${DIFFERENCE}s (estimate: ${ESTIMATE}s, actual: ${ACTUAL_DURATION}s)"
  exit 1
fi

echo "PASS: Time estimate accurate (estimate: ${ESTIMATE}s, actual: ${ACTUAL_DURATION}s)"
```
```

---

### Improvement 4: Add Failure Mode Injection

**Add section for each scenario:**

```markdown
#### Failure Mode Testing - Charlotte Tetris (Scenario C1)

**Purpose**: Verify system handles failures gracefully for Charlotte (must never see errors)

---

**Failure Mode 1: Backend Crash During Build**

*Setup*:
```bash
# Start normal build
PROJECT_ID=$(curl -s -X POST http://localhost:8000/api/projects ... | jq -r '.project_id')

# Wait 30s then kill backend
sleep 30
pkill -9 uvicorn
```

*Expected Behavior*:
- Frontend detects disconnection within 5s
- Shows user-friendly message: "Connection lost. Retrying..."
- Automatically reconnects when backend restarted
- Resumes build from last checkpoint
- Charlotte NEVER sees technical error

*Observable Checkpoints*:
- [ ] SSE connection drops (client detects)
- [ ] Frontend shows reconnection UI within 5s
- [ ] Database preserves build state (`status != "ERROR"`)
- [ ] After reconnect, build continues (new SSE events)
- [ ] No console errors visible to user

---

**Failure Mode 2: Generated Game Has JavaScript Error**

*Setup*:
```bash
# Artificially inject error into generated code
sed -i 's/function startGame/function startGame() { undefinedFunction(); /g' data/projects/{project_id}/game.html
```

*Expected Behavior*:
- Verification step CATCHES error
- Status set to "NEEDS_FIXES"
- Charlotte sees: "I need to fix something. Give me a moment..."
- System auto-attempts fix (retry loop)
- Eventually succeeds OR gracefully fails with clear message

*Observable Checkpoints*:
- [ ] Verification runs: `grep "Running verification" backend.log`
- [ ] Verification detects error: `grep "Verification failed.*undefinedFunction" backend.log`
- [ ] Status updated: `SELECT status FROM projects` returns "NEEDS_FIXES"
- [ ] Auto-retry initiated: `grep "Attempting fix" backend.log`
- [ ] User message appropriate: No technical jargon

---

**Failure Mode 3: Network Timeout During Prompt**

*Setup*:
```bash
# Add network delay to simulate timeout
tc qdisc add dev lo root netem delay 10000ms

# Submit request (will timeout)
curl --max-time 5 -X POST http://localhost:8000/api/projects ...
```

*Expected Behavior*:
- Request times out gracefully
- Charlotte sees: "That's taking a while. Let me try again."
- System retries automatically
- Does NOT create orphaned project in database

*Observable Checkpoints*:
- [ ] Request timeout handled: HTTP 408 or 504
- [ ] No orphaned projects: `SELECT COUNT(*) FROM projects WHERE status='PLANNING' AND updated_at < NOW() - INTERVAL 5 MINUTE` returns 0
- [ ] Frontend shows retry UI
- [ ] Second attempt succeeds after network restored
```

---

### Improvement 5: Add State Reset Procedures

**Add to beginning of document:**

```markdown
## Test Isolation and State Management

### Clean Slate Reset (Run Before Each Test)

**Purpose**: Ensure tests don't interfere with each other

**Reset Checklist**:
```bash
#!/bin/bash
# test_reset.sh - Run before each test

set -e

echo "🧹 Resetting test environment..."

# 1. Stop all services
pkill -f "uvicorn.*main:app" || true
pkill -f "npm.*dev" || true

# 2. Clean database
sqlite3 outcomist.db <<SQL
DELETE FROM projects WHERE name LIKE '%test%';
DELETE FROM sessions WHERE project_id NOT IN (SELECT id FROM projects);
DELETE FROM messages WHERE session_id NOT IN (SELECT id FROM sessions);
VACUUM;
SQL

echo "  ✓ Database cleaned"

# 3. Clean file system
rm -rf data/projects/*test*
rm -rf /tmp/outcomist_test_*.log
rm -rf /tmp/sse_events.log

echo "  ✓ File system cleaned"

# 4. Restart services
cd backend
.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "  ✓ Backend started (PID: $BACKEND_PID)"

cd ../frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  ✓ Frontend started (PID: $FRONTEND_PID)"

# 5. Wait for services to be ready
sleep 5
curl -s http://localhost:8000/health || { echo "Backend not ready"; exit 1; }
curl -s http://localhost:5173 || { echo "Frontend not ready"; exit 1; }

echo "✅ Test environment ready"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
```

---

### Improvement 6: Add Evidence Collection Template

**Add to each scenario:**

```markdown
#### Evidence Collection - Charlotte Tetris (Scenario C1)

**Artifacts to Capture**:

1. **Backend Logs**:
```bash
# Filter relevant log lines
grep -E "(charlotte-tetris-test|verification|status_update)" /tmp/backend.log > results/c1_backend.log
```

2. **SSE Event Stream**:
```bash
# Copy SSE events with timestamps
cp /tmp/sse_events.log results/c1_sse_events.log
```

3. **Database Snapshot**:
```bash
# Export project state at key moments
sqlite3 outcomist.db <<SQL > results/c1_database.txt
SELECT * FROM projects WHERE name LIKE 'charlotte-tetris-test%';
SELECT * FROM sessions WHERE project_id IN (SELECT id FROM projects WHERE name LIKE 'charlotte-tetris-test%');
SQL
```

4. **Generated Files**:
```bash
# Archive all generated files
tar czf results/c1_files.tar.gz data/projects/charlotte-tetris-test-*/
```

5. **Browser Screenshots**:
```bash
# Capture screenshots at key moments
npx playwright screenshot \
  --url "file://$(pwd)/data/projects/charlotte-tetris-test-123/game.html" \
  --output results/c1_game_screenshot.png
```

6. **Console Output**:
```bash
# Capture browser console
npx playwright test <<EOF
const page = await browser.newPage();
page.on('console', msg => fs.appendFileSync('results/c1_console.log', msg.text() + '\n'));
await page.goto('file://...');
await page.waitForTimeout(5000);
EOF
```

**Final Evidence Package**:
```
results/
├── c1_backend.log          # Backend log filtered
├── c1_sse_events.log        # SSE stream with timestamps
├── c1_database.txt          # Database state
├── c1_files.tar.gz          # Generated files
├── c1_game_screenshot.png   # Visual proof
├── c1_console.log           # Browser console
└── c1_summary.md            # Test summary (generate this)
```

**Auto-Generate Summary**:
```bash
cat > results/c1_summary.md <<EOF
# Test C1: Charlotte Tetris - Summary

**Execution Time**: $(date)
**Status**: PASS/FAIL

## Metrics
- Game works: ✅/❌
- Progress visible: ✅/❌
- Time accurate: ✅/❌
- No errors: ✅/❌
- Keyboard works: ✅/❌

## Timeline
$(grep -h "status_update" results/c1_sse_events.log | awk '{print $1, $3}')

## Files Generated
$(ls -lh data/projects/charlotte-tetris-test-*/*)

## Console Errors
$(wc -l < results/c1_console.log) errors detected
$(head -n 20 results/c1_console.log)

## Verdict
[Write detailed verdict here]
EOF
```
```

---

## Recommended Document Structure

**Proposed Reorganization**:

```markdown
# E2E Test Scenarios - Execution Guide

## Part 1: Test Infrastructure
- Setup and teardown scripts
- State reset procedures
- Log capture configuration
- Evidence collection templates

## Part 2: Test Execution Steps
For each scenario:
- Setup commands (exact bash)
- Observable checkpoints (exact log lines, status codes, DB queries)
- Success criteria (measurable)
- Failure modes (injection methods)
- Evidence collection (artifacts)

## Part 3: Test Scenarios
- Charlotte (3 scenarios with full execution detail)
- Mason (3 scenarios)
- Laura (3 scenarios)
- Cross-cutting (3 scenarios)

## Part 4: Results Analysis
- How to interpret evidence
- Common failure patterns
- Debugging procedures
- Escalation criteria
```

---

## Prioritized Improvements

### Priority 1 (Must Have for ANY E2E Testing)
1. ✅ Add exact setup/teardown commands
2. ✅ Replace subjective criteria with measurable checkpoints
3. ✅ Specify which logs/artifacts to capture
4. ✅ Add state reset procedure

### Priority 2 (Needed for Automated Testing)
5. ✅ Add Playwright/browser automation selectors
6. ✅ Add API endpoint specifications
7. ✅ Add database query specifications
8. ✅ Add timing thresholds

### Priority 3 (Needed for Robust Testing)
9. ✅ Add failure mode injection methods
10. ✅ Add evidence analysis procedures
11. ✅ Add common failure patterns
12. ✅ Add debugging procedures

---

## Example: Fully Specified Test

**See Improvement 3 above** for complete example of Charlotte Tetris with:
- Setup commands (bash)
- Observable checkpoints (exact log lines)
- Measurable success criteria
- Test automation code (Playwright)
- Evidence collection (artifacts)
- Failure mode injection

---

## Next Steps

1. **Choose 1 scenario** (suggest: Charlotte Tetris - simplest, highest priority)
2. **Rewrite with full execution detail** using templates above
3. **Validate with dry run** (agent executes against real system)
4. **Iterate based on findings**
5. **Template other scenarios** using proven format

---

## Questions for User

1. **Execution Method**: Manual via UI, Direct API calls, or Playwright automation?
2. **Test Environment**: Local dev, staging server, or Docker containers?
3. **Evidence Requirements**: What artifacts must be preserved? (logs, screenshots, videos?)
4. **Failure Tolerance**: Should tests fail fast or collect maximum evidence?
5. **Test Duration**: Is 5-10 minutes per scenario acceptable?

**Ready to rewrite first scenario with full execution detail once preferences confirmed.**
