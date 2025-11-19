# E2E Test Matrix - Game Verification System

**Purpose**: Prove verification works across diverse user types and scenarios
**Status**: DRAFT - Awaiting execution
**Last Updated**: 2025-11-19

---

## Test Matrix Design

**Structure**: 10 User Types × 3 Core Scenarios = 30 Test Cases

### Why This Matrix?

1. **User Diversity**: Different users will create different types of broken games
2. **Scenario Coverage**: Broken, working, and edge cases
3. **Real-world Validation**: Tests how verification handles actual user requests

---

## 10 End User Personas

| ID | Persona | Tech Level | Typical Request Style |
|----|---------|------------|----------------------|
| U1 | **Novice Parent** | Low | "Make a game for my kids" |
| U2 | **Curious Student** | Medium | "Create Snake game with score" |
| U3 | **Indie Dev** | High | "Build Breakout with power-ups" |
| U4 | **Teacher** | Medium | "Educational math game" |
| U5 | **Non-technical Manager** | Low | "Simple team building game" |
| U6 | **Gamer** | Medium | "Retro platformer like Mario" |
| U7 | **Designer** | Medium | "Minimalist puzzle game" |
| U8 | **Tinkerer** | High | "Game with physics engine" |
| U9 | **Child (via parent)** | Low | "Dinosaur catching game" |
| U10 | **Accessibility Advocate** | High | "Keyboard-only accessible game" |

---

## 3 Core Scenarios

### S1: Broken Game (Should FAIL Verification)
**Goal**: Verify that verification catches broken games
**Expected**: Status = "Needs fixes", user sees error message

### S2: Working Game (Should PASS Verification)
**Goal**: Verify that verification passes working games
**Expected**: Status = "Complete", no error messages

### S3: Edge Case (Behavior Varies)
**Goal**: Test unusual requests and edge conditions
**Expected**: System handles gracefully

---

## Complete Test Matrix (30 Tests)

### Scenario 1: Broken Games (10 tests)

| Test | User | Request | Expected Breakage | Expected Result |
|------|------|---------|-------------------|-----------------|
| **T1-S1** | U1 (Parent) | "Make a game for my kids" | Generic prompt → AI adds `undefinedFunction()` | ❌ FAIL: Console error detected |
| **T2-S1** | U2 (Student) | "Snake game with score" | Missing event listeners | ❌ FAIL: No interactive elements |
| **T3-S1** | U3 (Indie Dev) | "Breakout with complex physics" | Uncaught reference error | ❌ FAIL: Console error detected |
| **T4-S1** | U4 (Teacher) | "Math quiz game" | Syntax error in calculation | ❌ FAIL: JavaScript error |
| **T5-S1** | U5 (Manager) | "Team building trivia" | Undefined variable access | ❌ FAIL: Console error |
| **T6-S1** | U6 (Gamer) | "Platformer with enemies" | Animation frame error | ❌ FAIL: Runtime error |
| **T7-S1** | U7 (Designer) | "Minimalist puzzle" | CSS breaks layout | ❌ FAIL: Interactive elements hidden |
| **T8-S1** | U8 (Tinkerer) | "Physics simulation game" | Physics library not loaded | ❌ FAIL: Library error |
| **T9-S1** | U9 (Child) | "Catch dinosaurs game" | Click handler typo | ❌ FAIL: No interactive response |
| **T10-S1** | U10 (Advocate) | "Keyboard-accessible game" | Missing keyboard handlers | ❌ FAIL: No interactive elements |

### Scenario 2: Working Games (10 tests)

| Test | User | Request | Expected Behavior | Expected Result |
|------|------|---------|-------------------|-----------------|
| **T1-S2** | U1 (Parent) | "Simple color matching game" | Clean HTML, button works | ✅ PASS: No errors |
| **T2-S2** | U2 (Student) | "Basic Snake game" | Canvas + keyboard controls | ✅ PASS: Interactive elements found |
| **T3-S2** | U3 (Indie Dev) | "Well-structured Breakout" | Proper architecture | ✅ PASS: Clean execution |
| **T4-S2** | U4 (Teacher) | "Addition practice game" | Input fields + validation | ✅ PASS: Forms work |
| **T5-S2** | U5 (Manager) | "Click counter game" | Simple button increment | ✅ PASS: Event handlers work |
| **T6-S2** | U6 (Gamer) | "Side-scrolling runner" | Canvas animation | ✅ PASS: Animation loop works |
| **T7-S2** | U7 (Designer) | "Zen garden simulator" | Drag-drop elements | ✅ PASS: Mouse events work |
| **T8-S2** | U8 (Tinkerer) | "Gravity simulation" | Physics calculations | ✅ PASS: Math functions work |
| **T9-S2** | U9 (Child) | "Pop the balloons game" | Click detection | ✅ PASS: Click handlers work |
| **T10-S2** | U10 (Advocate) | "Tab-navigable game" | Keyboard focus | ✅ PASS: Keyboard events work |

### Scenario 3: Edge Cases (10 tests)

| Test | User | Request | Edge Case | Expected Result |
|------|------|---------|-----------|-----------------|
| **T1-S3** | U1 (Parent) | "Game with sounds" | Audio elements | ⚠️ WARN: Audio needs user interaction |
| **T2-S3** | U2 (Student) | "Multiplayer game" | WebSocket needed | ⚠️ WARN: Single-player fallback |
| **T3-S3** | U3 (Indie Dev) | "Save progress feature" | LocalStorage access | ✅ PASS: Storage works |
| **T4-S3** | U4 (Teacher) | "Print certificate button" | Window.print() | ✅ PASS: Print works |
| **T5-S3** | U5 (Manager) | "Share to social media" | External links | ✅ PASS: Links work |
| **T6-S3** | U6 (Gamer) | "Fullscreen mode" | Fullscreen API | ✅ PASS: Fullscreen works |
| **T7-S3** | U7 (Designer) | "Animated background" | CSS animations | ✅ PASS: Animations work |
| **T8-S3** | U8 (Tinkerer) | "WebGL game" | 3D rendering | ⚠️ WARN: Fallback to 2D |
| **T9-S3** | U9 (Child) | "Game with videos" | Video elements | ⚠️ WARN: Video autoplay blocked |
| **T10-S3** | U10 (Advocate) | "Screen reader hints" | ARIA labels | ✅ PASS: Accessibility markup |

---

## Execution Plan

### Phase 1: Quick Validation (2 tests)
**Goal**: Prove verification works at all

1. **T2-S1** (Broken Snake): Quick test, common request
2. **T2-S2** (Working Snake): Same game, should pass

**Time**: 10 minutes
**Deliverable**: Logs proving verification runs

### Phase 2: User Diversity (6 tests)
**Goal**: Test across different user types

- 3 Broken games from diverse users (U1, U5, U9)
- 3 Working games from diverse users (U1, U5, U9)

**Time**: 30 minutes
**Deliverable**: Evidence verification works for various requests

### Phase 3: Edge Cases (2 tests)
**Goal**: Handle unusual scenarios

- T3-S3 (LocalStorage)
- T6-S3 (Fullscreen)

**Time**: 15 minutes
**Deliverable**: Edge case handling documented

### Phase 4: Full Matrix (Optional)
**Goal**: Comprehensive validation

- All 30 tests executed
- Automated test runner created

**Time**: 2-3 hours
**Deliverable**: Complete test coverage

---

## Evidence Template

For each test, capture:

```markdown
### Test T{X}-S{Y}: {User} - {Scenario}

**Request**: "{exact prompt}"

**Backend Logs**:
```
[timestamp] 🔍 Running verification for game project...
[timestamp] 📊 Verification complete: passed={true/false}
[timestamp] {result message}
```

**UI State**:
- Status: {IDLE/PLANNING/WORKING/COMPLETE/etc}
- Status message: {message shown to user}

**Database**:
```sql
SELECT status FROM projects WHERE id = '{project_id}';
-- Result: {status}
```

**Files Created**:
- game.html (size: {bytes})
- [other files]

**Verdict**: ✅ PASS / ❌ FAIL / ⚠️ WARN

**Notes**: {observations}
```

---

## Success Criteria

### Minimum Viable Validation (Phase 1)
- [ ] 2 tests executed (1 broken, 1 working)
- [ ] Logs prove verification runs
- [ ] Broken game fails verification
- [ ] Working game passes verification

### Confidence Level (Phase 2)
- [ ] 8 tests executed (diverse users)
- [ ] Verification works across user types
- [ ] Error messages are clear

### Production Ready (Phase 3+)
- [ ] 10+ tests executed
- [ ] Edge cases handled
- [ ] Documentation complete
- [ ] Automated test runner created

---

## Implementation Notes

### How to Execute Tests

**Option A: Manual via UI** (realistic)
```bash
1. Start backend: cd outcomist/backend && .venv/bin/uvicorn src.main:app
2. Start frontend: cd outcomist/frontend && npm run dev
3. Open browser: http://localhost:5173
4. Create project, type prompt, observe
5. Capture logs from terminal
```

**Option B: Direct API** (faster)
```bash
# Use curl/httpie to hit streaming endpoint
# Monitor logs in real-time
# Query database for final state
```

**Option C: Automated** (future)
```python
# Pytest with Playwright
# Automated log capture
# Database assertions
```

---

## Current Status

- [ ] Matrix designed
- [ ] Phase 1 executed (2 tests)
- [ ] Phase 2 executed (6 tests)
- [ ] Phase 3 executed (2 tests)
- [ ] Evidence documented
- [ ] Verification validated

---

## Next Steps

1. **User approval** on test matrix design
2. **Execute Phase 1** (quick validation)
3. **Present evidence** to user
4. **Decide**: Continue with Phase 2+ or adjust approach

**Awaiting user approval to proceed...**
