# Manual E2E Test - Game Verification

**Purpose**: Verify that game verification runs during game generation
**Date**: 2025-11-19
**Tester**: Chris
**Status**: Ready to execute

---

## What We're Testing

Yesterday's issue: When you generated games, there were **NO verification logs**.

Today's fix: Added defensive logging and error handling.

**This test proves**: Do the verification logs appear now?

---

## Test Setup

### Terminal 1: Backend (with visible logs)
```bash
cd ~/amplifier/outcomist_collab/webapp/backend
.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Keep this terminal visible** - we need to see the logs!

### Terminal 2: Frontend
```bash
cd ~/amplifier/outcomist_collab/webapp/frontend
npm run dev
```

### Browser
```
Open: http://localhost:5173
```

---

## Test 1: Broken Game (Should FAIL Verification)

### Steps
1. Create new project (type: Game)
2. Enter prompt:
   ```
   Create a Snake game but intentionally add this line in the JavaScript:
   undefinedFunction();

   This will break the game for testing purposes.
   ```
3. Submit and **watch the backend terminal**

### Expected Backend Logs (Terminal 1)
Look for these EXACT log messages:

```
🔍 Running verification for game project {project-id}
📊 Verification complete: passed=False, errors=1, console_logs=X
🔍 Verification errors: ['Console error: ...undefinedFunction...']
❌ Verification FAILED: Console error: ...
```

### Expected UI Behavior
- Status should show "Needs fixes" or "Working" (NOT "Complete")
- User should see error message about verification failing

### ✅ Test 1 PASSES if:
- [ ] See `🔍 Running verification` in logs
- [ ] See `passed=False` in logs
- [ ] See error about `undefinedFunction`
- [ ] Project NOT marked "Complete"

### ❌ Test 1 FAILS if:
- [ ] NO verification logs appear
- [ ] Project marked "Complete" despite error
- [ ] No error message shown to user

---

## Test 2: Working Game (Should PASS Verification)

### Steps
1. Create new project (type: Game)
2. Enter prompt:
   ```
   Create a simple Snake game with:
   - Canvas element for the game board
   - Keyboard arrow controls
   - Score display
   - No errors or bugs
   ```
3. Submit and **watch the backend terminal**

### Expected Backend Logs (Terminal 1)
```
🔍 Running verification for game project {project-id}
📊 Verification complete: passed=True, errors=0, console_logs=X
✅ Verification PASSED - game is functional
```

### Expected UI Behavior
- Status should show "Complete"
- No error messages
- Game files should be created

### ✅ Test 2 PASSES if:
- [ ] See `🔍 Running verification` in logs
- [ ] See `passed=True` in logs
- [ ] See `✅ Verification PASSED` in logs
- [ ] Project marked "Complete"

### ❌ Test 2 FAILS if:
- [ ] NO verification logs appear
- [ ] Verification fails incorrectly
- [ ] Project not marked "Complete"

---

## Results Template

Copy this and fill it out:

```markdown
# E2E Test Results - Game Verification

**Date**: 2025-11-19
**Tester**: Chris
**Environment**: Local dev (macOS)

## Test 1: Broken Game

**Prompt Used**:
```
[paste your exact prompt]
```

**Backend Logs** (copy/paste the verification section):
```
[paste logs here]
```

**UI Status**: [e.g., "Needs fixes" / "Complete" / "Working"]

**Result**: ✅ PASS / ❌ FAIL

**Notes**:
-

---

## Test 2: Working Game

**Prompt Used**:
```
[paste your exact prompt]
```

**Backend Logs** (copy/paste the verification section):
```
[paste logs here]
```

**UI Status**: [e.g., "Complete"]

**Result**: ✅ PASS / ❌ FAIL

**Notes**:
-

---

## Overall Assessment

**Both tests passed**: ✅ / ❌

**Verification is working**: YES / NO

**Evidence quality**: [Strong / Weak / None]

**Next steps**:
-
```

---

## What Success Looks Like

### ✅ Complete Success
- Both tests show verification logs
- Broken game fails verification
- Working game passes verification
- Logs match expected format

### ⚠️ Partial Success
- Verification logs appear
- But behavior is incorrect (e.g., broken game passes)
- Indicates logic bug, not integration bug

### ❌ Complete Failure
- NO verification logs appear
- Same problem as yesterday
- Integration still broken

---

## Troubleshooting

### If NO logs appear:
1. Check backend is running on port 8000
2. Check you're creating a GAME project (not trip/content)
3. Check the game actually completes generation
4. Check for errors in backend console

### If verification crashes:
1. Look for exception traceback in logs
2. Check if Playwright is installed: `.venv/bin/playwright install`
3. Check file permissions on game files

### If unclear results:
1. Take screenshots of both logs and UI
2. Copy full backend log output
3. Note the exact project status

---

## After Testing

Share with me:
1. **The filled-out results template above**
2. **Screenshots of backend logs** (verification section)
3. **Screenshots of UI** (project status)

I'll analyze and determine:
- ✅ Fixed: Verification now works!
- ⚠️ Partial: Works but has bugs
- ❌ Broken: Same issue as yesterday

---

## Time Estimate

- Test 1: 2-3 minutes
- Test 2: 2-3 minutes
- Documentation: 2 minutes
- **Total: ~10 minutes**

---

**Ready to start when you are!** 🚀
