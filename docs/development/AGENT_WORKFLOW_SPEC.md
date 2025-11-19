# Multi-Agent Workflow Implementation Spec

**Status**: Ready to implement (Next Session)
**Priority**: HIGH - Core UX improvement
**Estimated Time**: 4-6 hours
**Dependencies**: Claude Agent SDK (already installed)

---

## Why This Matters

**Current Problem:**
User sees one blob of text: "I'll create... ✓files Your game is ready with..."

**Desired Experience (like Manus):**
```
Task 1: Planning ✓
  "Creating Tetris with:
   - 10×20 board
   - 7 pieces
   - Score tracking"

Task 2: Building 🔵 (0:45)
  ✓ index.html
  ✓ style.css
  ✓ script.js

Task 3: Verifying ⏱
  (pending)

Task 4: Complete ⏱
  (pending)
```

**The Solution:** Multi-agent workflow using Claude Agent SDK

---

## Architecture

### Agent Roles

**1. Planner Agent**
- **Input**: User request
- **Output**: Detailed plan with features, files, success criteria
- **UI Shows**: "Planning implementation" with plan details
- **Duration**: 10-30 seconds

**2. Builder Agent**
- **Input**: Plan from Planner
- **Output**: File operations (create/update files)
- **UI Shows**: "Creating files" with real-time file names
- **Duration**: 30-90 seconds

**3. Verifier Agent**
- **Input**: Files created + success criteria
- **Output**: Verification result (pass/fail + feedback)
- **UI Shows**: "Verifying output" with check results
- **Duration**: 10-20 seconds

**4. Coordinator** (Main Agent)
- Orchestrates the workflow
- Handles agent delegation
- Manages retry loop
- Emits SSE events for UI

---

## Implementation Steps

### Step 1: Create Subagent Definitions

**File Structure:**
```
webapp/backend/.claude/
└── agents/
    ├── planner.md
    ├── builder.md
    └── verifier.md
```

**planner.md:**
```markdown
# Planner Agent

You are a game planning specialist.

## Role
Analyze user requests and create detailed implementation plans.

## Output Format
Respond with a structured plan:

```
Planning: [Game Name]

Features:
- Feature 1
- Feature 2
- Feature 3

Files to create:
- index.html: Game structure and UI
- style.css: Visual design and layout
- script.js: Game logic and controls

Success criteria:
- Game loads without errors
- Controls respond correctly
- Score updates properly
```

Be specific and comprehensive. The builder will execute your plan exactly.
```

**builder.md:**
```markdown
# Builder Agent

You are a game implementation specialist.

## Role
Execute the plan and create working game files.

## Context
You receive:
- User's original request
- Detailed plan from Planner

## Instructions
1. Read the plan carefully
2. Create files using create_file tool
3. NO explanatory text - just create files
4. Files should be complete and ready to run

Output ONLY file creation tool calls. No narration.
```

**verifier.md:**
```markdown
# Verifier Agent

You are a quality verification specialist.

## Role
Test the created game and verify it works.

## Process
1. Check all success criteria from plan
2. Look for console errors
3. Verify interactive elements exist
4. Test game loads properly

## Output Format
```
Verification: [PASS/FAIL]

Checks:
✓ Game loads without errors
✓ Interactive elements present
✗ Controls not responding

[If FAIL]
Issues found:
- Specific issue 1
- Specific issue 2

Fixes needed:
- Update script.js: Add keyboard event listeners
- Update index.html: Fix button IDs
```

Be thorough but concise.
```

### Step 2: Create Workflow Coordinator

**File**: `webapp/backend/src/ai/workflow.py`

```python
"""Multi-agent workflow coordination using Claude Agent SDK"""

import logging
from dataclasses import dataclass
from typing import AsyncGenerator
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

logger = logging.getLogger(__name__)


@dataclass
class WorkflowState:
    """Track workflow progress"""
    request_id: str
    user_request: str
    plan: str | None = None
    files_created: list[str] = None
    verification_result: str | None = None
    retry_count: int = 0
    max_retries: int = 2


async def execute_game_workflow(
    user_request: str,
    project_id: str,
    session_id: str
) -> AsyncGenerator[dict, None]:
    """
    Execute multi-agent workflow for game creation

    Yields SSE events:
    - workflow_started: List of tasks
    - task_started: Agent begins work
    - task_progress: Agent progress update
    - task_completed: Agent finishes
    - task_retry: Verification failed, retrying
    - workflow_completed: All done
    """

    state = WorkflowState(
        request_id=f"wf_{session_id}",
        user_request=user_request
    )

    # Emit workflow start
    yield {
        "type": "workflow_started",
        "tasks": [
            {"id": "task_1", "label": "Planning implementation", "agent": "planner"},
            {"id": "task_2", "label": "Creating game files", "agent": "builder"},
            {"id": "task_3", "label": "Verifying output", "agent": "verifier"},
            {"id": "task_4", "label": "Complete", "agent": "coordinator"},
        ]
    }

    # Task 1: Planner
    yield {"type": "task_started", "task_id": "task_1", "agent": "planner"}

    options = ClaudeAgentOptions(
        working_directory=f"/path/to/projects/{project_id}",
        allowed_tools=["Read"],  # Planner only needs to read, not write
    )

    async with ClaudeSDKClient(options=options) as planner:
        prompt = f"""Analyze this request and create a detailed plan:

{user_request}

Output a structured plan following your instructions."""

        await planner.query(prompt)

        plan_text = ""
        async for msg in planner.receive_response():
            if msg.type == "assistant":
                plan_text += msg.content
                # Stream plan to user
                yield {
                    "type": "task_progress",
                    "task_id": "task_1",
                    "content": msg.content
                }

        state.plan = plan_text

    yield {"type": "task_completed", "task_id": "task_1"}

    # Task 2: Builder (with retry loop)
    build_attempt = 0
    while build_attempt <= state.max_retries:
        yield {"type": "task_started", "task_id": "task_2", "agent": "builder"}

        builder_options = ClaudeAgentOptions(
            working_directory=f"/path/to/projects/{project_id}",
            allowed_tools=["Write", "Edit"],  # Builder can write files
        )

        async with ClaudeSDKClient(options=builder_options) as builder:
            # Build context for builder
            context = f"""Original request: {user_request}

Plan from Planner:
{state.plan}"""

            if state.verification_result and "FAIL" in state.verification_result:
                context += f"""

Previous verification FAILED:
{state.verification_result}

Fix the issues and rebuild."""

            await builder.query(context)

            files = []
            async for msg in builder.receive_response():
                # Track file creation
                if "create_file" in str(msg):
                    # Extract filename
                    yield {
                        "type": "task_progress",
                        "task_id": "task_2",
                        "content": "Creating files..."
                    }
                files.append(msg)

            state.files_created = files

        yield {"type": "task_completed", "task_id": "task_2"}

        # Task 3: Verifier
        yield {"type": "task_started", "task_id": "task_3", "agent": "verifier"}

        verifier_options = ClaudeAgentOptions(
            working_directory=f"/path/to/projects/{project_id}",
            allowed_tools=["Read", "Bash"],  # Verifier can read and run tests
        )

        async with ClaudeSDKClient(options=verifier_options) as verifier:
            verification_prompt = f"""Verify the game files against the plan:

Plan:
{state.plan}

Check each success criterion and report results."""

            await verifier.query(verification_prompt)

            verification_text = ""
            async for msg in verifier.receive_response():
                verification_text += str(msg)

            state.verification_result = verification_text

        yield {"type": "task_completed", "task_id": "task_3"}

        # Check if verification passed
        if "PASS" in state.verification_result:
            break  # Success!
        else:
            build_attempt += 1
            if build_attempt <= state.max_retries:
                yield {
                    "type": "task_retry",
                    "task_id": "task_2",
                    "retry_count": build_attempt,
                    "reason": "Verification failed"
                }
                # Loop back to builder
            else:
                # Max retries exceeded
                yield {
                    "type": "workflow_failed",
                    "reason": "Max retries exceeded",
                    "details": state.verification_result
                }
                return

    # Task 4: Complete
    yield {
        "type": "workflow_completed",
        "status": "success",
        "summary": "Game created and verified"
    }
```

### Step 3: Update streaming.py

**Changes to `webapp/backend/src/ai/streaming.py`:**

```python
# Add import
from .workflow import execute_game_workflow

# In stream_claude_response function, replace current implementation with:

async def stream_claude_response(...):
    """Stream AI response using multi-agent workflow"""

    # Check if this is a game project
    if session.project.type == ProjectType.GAME:
        # Use multi-agent workflow
        async for event in execute_game_workflow(
            user_message,
            str(session.project_id),
            str(session_id)
        ):
            # Convert workflow events to SSE format
            yield format_sse_event(
                SSEEventType.STATUS_UPDATE,
                event
            )
    else:
        # Use original single-agent flow for non-game projects
        # ... existing code ...
```

### Step 4: Update Frontend to Handle Workflow Events

**Changes to `webapp/frontend/src/components/project/ProjectCard.tsx`:**

```typescript
// In SSE event handling:

if (parsed.type === 'workflow_started') {
  // Initialize task list from workflow tasks
  const dynamicTasks = parsed.tasks.map((t, i) => ({
    id: t.id,
    label: t.label,
    state: 'pending' as TaskState,
    order: i
  }));
  setTasks(dynamicTasks);
}

if (parsed.type === 'task_started') {
  // Mark task as active
  updateTaskById(parsed.task_id, {
    state: 'active',
    startedAt: Date.now()
  });
}

if (parsed.type === 'task_progress') {
  // Update task status message
  updateTaskById(parsed.task_id, {
    statusMessage: parsed.content || parsed.message
  });
}

if (parsed.type === 'task_completed') {
  // Mark task as complete
  updateTaskById(parsed.task_id, {
    state: 'completed',
    completedAt: Date.now()
  });
}

if (parsed.type === 'task_retry') {
  // Show retry indicator
  updateTaskById(parsed.task_id, {
    state: 'active',
    statusMessage: `Retry ${parsed.retry_count}: ${parsed.reason}`
  });
}
```

### Step 5: Testing Strategy

**Unit Tests:**
```python
# tests/test_workflow.py

@pytest.mark.asyncio
async def test_planner_agent():
    """Test planner creates valid plan"""
    # Run planner in isolation
    # Verify plan has required structure

@pytest.mark.asyncio
async def test_builder_agent():
    """Test builder creates files from plan"""
    # Give builder a plan
    # Verify files are created

@pytest.mark.asyncio
async def test_verifier_agent():
    """Test verifier catches broken games"""
    # Give verifier broken files
    # Verify it fails with feedback

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete workflow end-to-end"""
    # Run full workflow
    # Verify all agents execute
    # Verify files created and verified
```

**Integration Test:**
1. Start app
2. Create game via UI
3. Watch for 4 distinct tasks in task progress card
4. Verify each agent's output appears
5. Confirm final game works

---

## File Checklist

**New Files to Create:**
- [ ] `webapp/backend/.claude/agents/planner.md`
- [ ] `webapp/backend/.claude/agents/builder.md`
- [ ] `webapp/backend/.claude/agents/verifier.md`
- [ ] `webapp/backend/src/ai/workflow.py`
- [ ] `webapp/backend/tests/test_workflow.py`

**Files to Modify:**
- [ ] `webapp/backend/src/ai/streaming.py` - Add workflow integration
- [ ] `webapp/frontend/src/hooks/useTaskProgress.ts` - Support dynamic tasks
- [ ] `webapp/frontend/src/components/project/ProjectCard.tsx` - Handle workflow events

---

## Expected Benefits

**User Experience:**
- ✅ Clear visibility into each phase
- ✅ Understand what's being built (plan detail)
- ✅ See real progress (not fake steps)
- ✅ Automatic quality checking
- ✅ Automatic retry on failure

**Code Quality:**
- ✅ Separation of concerns (planning vs building vs testing)
- ✅ Testable agents (each can be tested independently)
- ✅ Retry logic built-in
- ✅ Better error handling

**Development:**
- ✅ Easy to add new agent types (Designer, Optimizer, etc.)
- ✅ Easy to customize agent prompts
- ✅ Clean integration with existing UI

---

## Risks & Mitigations

**Risk 1: SDK learning curve**
- Mitigation: Start with simple examples, reference SDK docs

**Risk 2: Longer generation time**
- Mitigation: 3 agents sequentially ~2-3min total (acceptable)

**Risk 3: Agent coordination bugs**
- Mitigation: Comprehensive testing at each layer

**Risk 4: Breaking existing functionality**
- Mitigation: Keep old flow for non-game projects, add workflow only for games

---

## Success Criteria

✅ **Must Have:**
- [ ] User sees 4 distinct tasks in UI
- [ ] Each task shows appropriate content
- [ ] Games are automatically verified
- [ ] Verification failures trigger retry
- [ ] Final games work properly

✅ **Nice to Have:**
- [ ] Plan extraction for task labels
- [ ] Detailed verification feedback
- [ ] Configurable retry count
- [ ] Agent performance metrics

---

## Next Session Checklist

1. **Read this spec** to refresh context
2. **Review Agent SDK docs** (bookmarked above)
3. **Create subagent definitions** (planner, builder, verifier)
4. **Implement workflow coordinator** in workflow.py
5. **Update streaming.py** to use workflow for games
6. **Update frontend** to handle workflow events
7. **Test thoroughly** - unit tests, integration, E2E
8. **Deploy and validate** with real game creation

**Estimated timeline:**
- Setup & agent definitions: 1 hour
- Workflow implementation: 2 hours
- Frontend integration: 1 hour
- Testing & debugging: 2 hours
- **Total: 6 hours**

---

## Resources

**Claude Agent SDK:**
- Docs: https://platform.claude.com/docs/en/api/agent-sdk/overview
- Python SDK: https://github.com/anthropics/claude-agent-sdk-python
- Installation: `uv add claude-agent-sdk` ✅ DONE

**Current Code:**
- SSE events: `webapp/backend/src/ai/events.py`
- Status handling: `webapp/backend/src/ai/status.py`
- Task progress card: `webapp/frontend/src/components/project/TaskProgressCard.tsx`
- Task hook: `webapp/frontend/src/hooks/useTaskProgress.ts`

**Related Design:**
- Zen-architect's workflow design (in this session's agent output)
- Manus screenshots (reference for UX)

---

## Notes from This Session

**What Works:**
- Task progress card UI is ready
- SSE infrastructure in place
- Status badge system works
- Real-time updates work

**What Needs Work:**
- Replace single-agent flow with multi-agent
- Extract dynamic tasks from workflow (not hardcoded)
- Wire up agent delegation properly
- Add verification retry loop

**User Feedback Addressed:**
- ✅ Manus-style visibility
- ✅ Collapsed task bar by default
- ✅ Shows actual activity
- ✅ Clean response structure needed (agents will fix this)

---

**Ready to implement in next session!** 🚀
