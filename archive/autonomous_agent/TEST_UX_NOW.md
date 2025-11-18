# Test UX Now - 5-Minute Quick Start

## Prerequisites Check

```bash
# 1. Check backend is running
curl http://localhost:8000
# Should return: {"message": "Autonomous Agent API"}

# 2. Check frontend is running
curl http://localhost:5173
# Should return HTML

# 3. Check API key is set
echo $ANTHROPIC_API_KEY
# Should show your key (not empty)
```

If any fail:
- **Backend**: `cd autonomous_agent && uvicorn src.api:app --reload`
- **Frontend**: `cd autonomous_agent/web && npm run dev`
- **API Key**: `export ANTHROPIC_API_KEY=your_key_here`

---

## Test 1: Simple Task (2 minutes)

### Open the app
```
http://localhost:5173
```

### Submit this task
```
Generate 3 motivational quotes about productivity.
Output as JSON with fields: quote, author, category.
```

### What to observe
- ✅ Form feels intuitive
- ✅ "Delegate Task" button is clear
- ✅ Redirects to progress automatically
- ✅ Progress pipeline shows stages
- ✅ Results appear with download button
- ✅ Verification badge shows confidence

### Expected result
JSON file with 3 quotes downloads successfully.

### Time estimate
~30-60 seconds

---

## Test 2: Realistic Scenario (3 minutes)

### Submit this task
```
Goal: Draft 5 Facebook ad headlines for a productivity app.

Constraints:
- Each headline must be under 40 characters
- Each must include the phrase "Save Time"
- All must be unique
- Output as JSON
```

### What to observe
- ✅ Progress shows "Planning" step
- ✅ Progress shows "Executing" step
- ✅ Progress shows "Verifying" step
- ✅ Verification checks character count
- ✅ Verification checks for "Save Time"
- ✅ JSON downloads correctly

### Expected result
JSON file with 5 compliant headlines.

### Time estimate
~45-90 seconds

---

## Quick Evaluation Questions

After running both tests, answer these:

### 1. First Impression
**Does the landing page make it clear what this does?**
- [ ] Yes, immediately
- [ ] Sort of
- [ ] No, confusing

### 2. Trust
**Would you use the output without reviewing it?**
- [ ] Yes (Scenario 1)
- [ ] Yes (Scenario 2)
- [ ] No, need to review

### 3. Comparison
**How does this compare to using ChatGPT for the same task?**
- [ ] Better
- [ ] Same
- [ ] Worse

**Why?**
```
(Write 1 sentence)
```

### 4. Delegation Feel
**Does this feel like delegating work or asking for help?**
- [ ] Delegating (like assigning to a person)
- [ ] Asking for help (like a tool)
- [ ] Not sure

### 5. One Thing
**What ONE thing would make this better?**
```
(Write 1 sentence)
```

---

## If You Find Issues

### Critical (Can't complete task)
```
Issue:

Screenshot/Description:

```

### Annoying (Can complete but frustrated)
```
Issue:

Screenshot/Description:

```

### Polish (Works fine but could be better)
```
Issue:

Suggestion:

```

---

## Next Step Decision

### ✅ If both tests worked smoothly
→ Ready for real user testing
→ Recruit 5 users for full scenarios

### ⚠ If one test had issues
→ Fix the issues first
→ Re-test yourself
→ Then recruit users

### ❌ If both tests failed
→ Review backend logs
→ Check browser console
→ Fix critical bugs before user testing

---

## Backend Logs (If Debugging)

```bash
# Watch backend logs in real-time
cd autonomous_agent
uvicorn src.api:app --reload --log-level debug
```

Look for errors during:
- Task submission
- Planning step
- Execution step
- Verification step

---

## Browser Console (If Debugging)

Open browser DevTools (F12):

### Check for errors
- **Console tab**: JavaScript errors?
- **Network tab**: API calls failing?
- **Application tab**: localStorage issues?

### Common issues
- **CORS errors**: Backend needs to allow http://localhost:5173
- **404 errors**: Backend endpoint mismatch
- **Timeout errors**: LLM call taking too long

---

## Pro Tips

### Fastest test cycle
1. Keep browser DevTools open (F12)
2. Keep terminal with backend logs visible
3. Submit task
4. Watch both console and terminal
5. If error → Fix → Refresh → Retry

### What "good" looks like
- Task completes in <2 minutes
- No console errors
- Verification shows 80%+ confidence
- Artifact downloads without errors
- You feel confident using the output

### What "bad" looks like
- Task takes >5 minutes
- Console shows errors
- Verification fails
- Can't download artifact
- You don't trust the output

---

## Results Template

After testing, fill this out:

```
Date: [TODAY]
Tester: [YOUR NAME]

Test 1 (Simple):
- Status: [PASS/FAIL]
- Time: [XX seconds]
- Trust: [YES/NO]
- Issue: [IF ANY]

Test 2 (Realistic):
- Status: [PASS/FAIL]
- Time: [XX seconds]
- Trust: [YES/NO]
- Issue: [IF ANY]

Overall:
- Would I use this? [YES/NO]
- One improvement: [WHAT]
- Ready for users? [YES/NO]
```

---

## Decision Tree

```
Did both tests pass?
├─ YES
│  └─ Do you trust the output?
│     ├─ YES → ✅ READY FOR USER TESTING
│     └─ NO → Why not? Fix trust issues first
│
└─ NO
   └─ What failed?
      ├─ Backend error → Fix backend, retry
      ├─ Frontend error → Fix frontend, retry
      ├─ Slow performance → Optimize, retry
      └─ Confusing UX → Revise, retry
```

---

## Quick Checklist

Before calling others to test:

- [ ] Backend running and accessible
- [ ] Frontend running and accessible
- [ ] API key configured
- [ ] Simple task completes successfully
- [ ] Realistic task completes successfully
- [ ] Artifacts download correctly
- [ ] No console errors
- [ ] No backend errors
- [ ] You trust the output
- [ ] UX feels intuitive

**All checked?** → You're ready for user testing!

**Any unchecked?** → Fix those first!

---

*Time to complete this guide: 5-10 minutes*
*Goal: Confidence to invite real users*
