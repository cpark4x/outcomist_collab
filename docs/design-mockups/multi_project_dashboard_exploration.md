# Multi-Project Dashboard Exploration

**Based on mockup analysis: Parallel project management with output-first visibility**

---

## Mockup Analysis

### What the Mockup Shows

**Three concurrent projects with different states:**

1. **New Claude Session** (Running...)
   - Shows terminal/code execution view
   - Traditional Claude Code interface
   - Status: Active execution in progress

2. **Remember12** (Complete.)
   - Shows actual deliverable (photo gallery layout)
   - No code/terminal visible - just the output
   - Status: Finished, artifact ready

3. **Outcomist** (AI is asking for me to answer a question)
   - Shows Claude interface with decision pending
   - Clear indication that human input needed
   - Status: Blocked, waiting for user response

### Key Innovation Points

1. **Multi-Project Awareness** - User can work on 3+ projects simultaneously
2. **Context-Appropriate Views** - Each project shows what matters most at that moment
3. **Status-Driven Presentation** - Running code vs. Completed artifact vs. Needs input
4. **Output-First for Completed Work** - Shows the actual deliverable, not the process

### What's NOT Visible (but mentioned)
- Multiple tasks/tabs within a single project
- Task orchestration within a project
- Notification system for state changes

---

## Design Implications for Autonomous Agent

This mockup reveals a **meta-layer** above our 5 UX proposals. The proposals focused on single-project task management, but users need **multi-project orchestration**.

### The Missing Layer: Portfolio View

Our 5 proposals all assume "you're working in one project." But this mockup shows reality:
- **People work on multiple projects concurrently**
- **Each project has different states requiring different actions**
- **The interface should adapt to what matters most per project**

---

## Proposal 6: Mission Command (Multi-Project Orchestration)

### Core Metaphor
**Airport terminal departures board + Project portfolio dashboard**

Users manage a portfolio of autonomous projects. Each project is a "flight" with its own status, and the interface helps users monitor all flights while drilling into specifics when needed.

---

## Key Screens

### 1. Portfolio Dashboard (Home)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  🚀 Autonomous Agent - Portfolio View                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Active Projects                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ New Claude   │  │ Remember12   │  │ Outcomist    │ │
│  │ Session      │  │              │  │              │ │
│  │ [Running...] │  │ [Complete]   │  │ [Needs You]  │ │
│  │              │  │              │  │              │ │
│  │ [Preview]    │  │ [Artifact]   │  │ [Respond]    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  Queued Projects (2)                    [+ New Project] │
└─────────────────────────────────────────────────────────┘
```

**Interaction Model:**
- **Project cards** show appropriate preview based on state
- **Running projects:** Show live execution preview (terminal, logs, progress)
- **Complete projects:** Show artifact preview (photo gallery, report, dashboard)
- **Blocked projects:** Show what's needed (answer question, approve plan, provide files)

**Card States:**

| State | What User Sees | Primary Action |
|-------|---------------|----------------|
| **Running** | Live execution preview, progress % | "View Details" |
| **Complete** | Artifact thumbnail/preview | "Open Artifact" or "Download" |
| **Needs Input** | Question or approval request | "Respond" (badge count) |
| **Planning** | Agent thinking, estimating time | "Monitor" |
| **Failed** | Error summary | "View Logs" or "Retry" |
| **Paused** | Last known state | "Resume" or "Cancel" |

---

### 2. Project Deep Dive (Context Switch)

When user clicks a project card, they enter that project's context using **one of the 5 UX paradigms**:

**Routing Logic:**
```
User clicks "New Claude Session" (Running)
  → Opens Mission Control view (Proposal 1)
  → Shows real-time pipeline + execution logs

User clicks "Remember12" (Complete)
  → Opens Artifact Gallery (simplified Delegation Desk - Proposal 2)
  → Shows photo gallery with "Edit" or "Create Variant" options

User clicks "Outcomist" (Needs You)
  → Opens Hybrid Chat (Proposal 5)
  → Question/approval request at top, user can respond
```

**Key Innovation:** Portfolio dashboard is the **router**, and each project uses the UX paradigm most appropriate for its current state.

---

### 3. Multi-Tab Task Management (Within a Project)

**Visible when inside a project:**

```
┌─────────────────────────────────────────────────────────┐
│  Project: Remember12                         [← Back]   │
├─────────────────────────────────────────────────────────┤
│  📑 Tasks:  [Photo Gallery ✓] [Timeline ⏳] [Export]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Task: Photo Gallery - COMPLETE]                       │
│  [Artifact preview shown here]                          │
│                                                          │
│  [Task: Timeline - IN PROGRESS]                         │
│  Agent is generating timeline visualization...          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Multiple tasks within a project:**
- Each task is a tab or expandable card
- User can monitor parallel task execution
- Tasks can have dependencies (Timeline needs Photo Gallery complete)
- Agent automatically orchestrates task order

---

### 4. Notification & Attention System

**When AI needs user input:**

**Portfolio View:**
- Project card shows **badge** with count: "2 questions pending"
- Project card highlights with **pulsing border** (subtle, not annoying)
- Top nav shows **inbox icon** with total count across all projects

**Project View:**
- Specific task/question highlighted
- "Respond to continue" prompt
- Option to "Skip for now" (agent pauses, doesn't fail)

**Notification Examples:**
```
🔔 Outcomist needs approval: "Should I use design approach A or B?"
🔔 New Claude Session waiting: "File upload required to continue"
🔔 Remember12 complete: "Photo gallery ready for review"
```

---

## Design Patterns from Mockup

### 1. State-Driven Presentation

**Principle:** Show what matters most for the current state.

| Project State | What User Needs | What UI Shows |
|--------------|----------------|---------------|
| **Running** | Confidence it's working | Live preview, progress indicator |
| **Complete** | Access to deliverable | Artifact front-and-center |
| **Needs Input** | What's being asked | Question/prompt prominently |
| **Failed** | What went wrong | Error summary, retry option |

**Anti-pattern:** Showing the same UI (logs/code) regardless of state.

---

### 2. Output-First for Completed Work

**From mockup:** Remember12 shows the photo gallery, NOT the code that generated it.

**Principle:** When work is done, the artifact IS the product. Process is secondary.

**Implementation:**
```
Complete Project Card:
┌──────────────────────┐
│ Remember12           │
│ Photo Gallery        │
│                      │
│ [Artifact Preview]   │
│ 📸 24 photos         │
│ ✓ All memories       │
│                      │
│ [Open] [Download]    │
│ [View Process]       │ ← Hidden by default
└──────────────────────┘
```

**"View Process" expander:**
- Shows execution logs
- Shows Planner → Executor → Verifier audit trail
- Available for transparency but not the default

---

### 3. Context-Appropriate Interaction

**From mockup:** Each project has different actions based on state.

| Project | State | Primary Action |
|---------|-------|----------------|
| New Claude Session | Running | "View Live Execution" |
| Remember12 | Complete | "Open Gallery" or "Download" |
| Outcomist | Needs Input | "Answer Question" |

**Principle:** The interface adapts to what the user can/should do next.

---

### 4. Multi-Project Status At-a-Glance

**Borrowing from airport departures board:**

```
┌─────────────────────────────────────────────────────────┐
│  Active Projects (5)                                    │
├──────────────────┬─────────────┬────────────┬──────────┤
│ Project          │ Status      │ Progress   │ Action   │
├──────────────────┼─────────────┼────────────┼──────────┤
│ New Claude Sess  │ ⏳ Running  │ ████░░ 65% │ [View]   │
│ Remember12       │ ✓ Complete  │ ██████100% │ [Open]   │
│ Outcomist        │ ⚠ Needs You │ ████░░ 70% │ [Respond]│
│ Sales Analysis   │ 📋 Planning │ ░░░░░░  5% │ [Monitor]│
│ Market Research  │ ⏸ Paused    │ ███░░░ 45% │ [Resume] │
└──────────────────┴─────────────┴────────────┴──────────┘
```

**List view option** for users managing 10+ projects.

---

## Integration with Original 5 Proposals

### Portfolio Dashboard as "Meta-UX"

The portfolio dashboard sits **above** the 5 UX proposals:

```
Portfolio Dashboard (Proposal 6)
    │
    ├─ Project A (uses Mission Control - Proposal 1)
    ├─ Project B (uses Delegation Desk - Proposal 2)
    ├─ Project C (uses Hybrid Chat - Proposal 5)
    └─ Project D (uses Timeline Narrative - Proposal 4)
```

**User can:**
1. Choose default UX paradigm per project
2. Or let system auto-select based on project type:
   - Technical/complex → Mission Control
   - Simple/outcome-focused → Delegation Desk
   - First-time/conversational → Hybrid Chat
   - Audit-required → Timeline Narrative

---

## Advanced Multi-Project Features

### 1. Cross-Project Context Sharing

**Scenario:** User working on "Market Research" and "Sales Deck" projects.

**Smart linking:**
- Sales Deck agent detects Market Research is complete
- Suggests: "I see you finished market research. Should I use those insights in the deck?"
- User approves → Agent pulls data from completed project

**UI:**
```
┌─────────────────────────────────────────────┐
│ Sales Deck - Planning                       │
│                                             │
│ 🔗 Related Project Detected                │
│ "Market Research" completed 2 hours ago     │
│                                             │
│ [ ] Use market research insights in deck   │
│ [ ] Reference competitor analysis section  │
│                                             │
│ [Apply Selected] [Ignore]                  │
└─────────────────────────────────────────────┘
```

---

### 2. Resource Allocation & Prioritization

**Scenario:** User starts 5 projects simultaneously.

**Portfolio Dashboard shows:**
```
Resource Allocation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CPU:  ████████░░░░ 65% (3 projects active)
Queue: 2 projects waiting for resources

Priority Order:
1. New Claude Session (High - user watching)
2. Outcomist (High - blocked on user input)
3. Sales Analysis (Medium - can wait)
4. Market Research (Low - background)
5. Report Export (Low - quick task)
```

**User can:**
- Drag to reorder priority
- Pause low-priority projects to free resources
- Set auto-priority rules ("Always prioritize projects with deadlines")

---

### 3. Project Templates & Cloning

**From completed project:**
```
Remember12 [Complete]
  └─ Actions:
      [Download Artifact]
      [View Execution Log]
      [Create Template] ← New
      [Clone Project]   ← New
```

**"Create Template" saves:**
- Project structure
- Task breakdown
- Success criteria
- Agent configuration

**"Clone Project" creates:**
- New project with same structure
- Different inputs/context files
- Example: "Remember12 for vacation photos" → Clone → "Remember12 for graduation"

---

### 4. Batch Operations

**Select multiple projects:**
```
☑ New Claude Session
☑ Sales Analysis
☐ Market Research

Batch Actions:
[Pause All] [Export All] [Delete All] [Change Priority]
```

---

## Technical Architecture Implications

### State Management

**Portfolio-level state:**
```json
{
  "portfolio_id": "user_12345",
  "projects": [
    {
      "project_id": "new_claude_session",
      "name": "New Claude Session",
      "state": "running",
      "progress": 0.65,
      "active_tasks": [
        {
          "task_id": "amplifier_analysis",
          "status": "executing",
          "stage": "executor"
        }
      ],
      "attention_needed": false,
      "selected_ux_paradigm": "mission_control"
    },
    {
      "project_id": "remember12",
      "name": "Remember12",
      "state": "complete",
      "progress": 1.0,
      "artifact": {
        "type": "photo_gallery",
        "url": "/artifacts/remember12_gallery.html",
        "preview_image": "/previews/remember12.jpg"
      },
      "attention_needed": false,
      "selected_ux_paradigm": "delegation_desk"
    },
    {
      "project_id": "outcomist",
      "name": "Outcomist",
      "state": "needs_input",
      "progress": 0.70,
      "attention_needed": true,
      "pending_questions": [
        {
          "question_id": "decision_001",
          "prompt": "Which design approach should I use?",
          "options": ["A", "B", "C"]
        }
      ],
      "selected_ux_paradigm": "hybrid_chat"
    }
  ]
}
```

### Real-Time Updates

**WebSocket events:**
```javascript
// Portfolio-level events
socket.on('project_state_changed', (data) => {
  // Update project card in portfolio view
  updateProjectCard(data.project_id, data.new_state);
});

socket.on('attention_needed', (data) => {
  // Show notification badge
  showAttentionBadge(data.project_id, data.reason);
});

socket.on('artifact_ready', (data) => {
  // Show completion notification
  // Switch card view to show artifact preview
  showArtifactPreview(data.project_id, data.artifact_url);
});
```

---

## Visual Design Exploration

### Portfolio Dashboard Layout Options

#### Option A: Card Grid (Like Mockup)
```
┌────────┐ ┌────────┐ ┌────────┐
│Project │ │Project │ │Project │
│   A    │ │   B    │ │   C    │
│Running │ │Complete│ │NeedsYou│
└────────┘ └────────┘ └────────┘

┌────────┐ ┌────────┐
│Project │ │+ New   │
│   D    │ │Project │
│Queued  │ │        │
└────────┘ └────────┘
```

**Pros:**
- Visual, scannable
- Shows previews/artifacts well
- Familiar pattern (like Trello, Asana)

**Cons:**
- Harder to compare projects side-by-side
- Takes more vertical space

---

#### Option B: List View (Departures Board)
```
┌─────────────────┬────────────┬─────────┬────────┐
│ Project         │ Status     │ Progress│ Action │
├─────────────────┼────────────┼─────────┼────────┤
│ New Claude Sess │ ⏳ Running │ ████ 65%│ [View] │
│ Remember12      │ ✓ Complete │ ████100%│ [Open] │
│ Outcomist       │ ⚠ NeedsYou │ ███  70%│ [Reply]│
└─────────────────┴────────────┴─────────┴────────┘
```

**Pros:**
- Compact, shows many projects at once
- Easy to compare status/progress
- Quick scanning for attention-needed items

**Cons:**
- Less visual
- Can't show artifact previews inline

---

#### Option C: Hybrid (Recommended)

**Default: Card grid** for 1-6 projects
**Toggle to list view** for 7+ projects

**Split screen option:**
```
┌─────────────────┬─────────────────────────┐
│ Portfolio List  │ Selected Project Detail │
│                 │                         │
│ □ Project A     │ [Live execution view]   │
│ ☑ Project B ←───┤                         │
│ □ Project C     │                         │
│ □ Project D     │                         │
└─────────────────┴─────────────────────────┘
```

---

## Notification System Design

### Attention Hierarchy

**Critical (Blocking):**
- 🔴 Agent failed, needs debugging
- 🔴 Deployment about to go live, needs approval

**High (Action Needed Soon):**
- 🟡 Agent asking question, work paused
- 🟡 Artifact ready for review before proceeding

**Medium (FYI):**
- 🟢 Project completed successfully
- 🟢 Milestone reached (50%, 75%)

**Low (Background):**
- 🔵 Project started
- 🔵 Stage transition (Plan → Execute)

### Notification Delivery

**In-app:**
- Badge counts on project cards
- Toast notifications for state changes
- Inbox/notification center for history

**Optional external:**
- Email for completed projects
- Slack/Teams for attention-needed items
- SMS for critical failures (if user enables)

---

## Comparison: Portfolio View vs. Original 5 Proposals

| Feature | Original 5 | Proposal 6 (Portfolio) |
|---------|-----------|------------------------|
| **Scope** | Single project | Multiple projects |
| **Focus** | Task execution detail | Cross-project orchestration |
| **Primary View** | Project-specific | Portfolio dashboard |
| **State Awareness** | Within project | Across all projects |
| **Navigation** | Task-to-task | Project-to-project |
| **Attention Mgmt** | Implicit | Explicit (badges, notifications) |

**Relationship:**
- Portfolio View is the **meta-layer** for multi-project users
- Original 5 proposals are the **deep-dive layers** for individual projects
- User flows: Portfolio → Select Project → Use appropriate UX paradigm

---

## User Scenarios

### Scenario 1: Morning Check-In

**User opens Autonomous Agent:**

1. **Portfolio Dashboard loads** (3 projects visible)
2. **Sees immediately:**
   - "Remember12" completed overnight ✓
   - "New Claude Session" still running from yesterday ⏳
   - "Outcomist" needs answer ⚠ (badge: 1 question)
3. **Actions:**
   - Click "Remember12" → Artifact opens (photo gallery)
   - Download/share gallery
   - Back to portfolio
   - Click "Outcomist" → Chat opens with question
   - Answer question → Agent resumes work
4. **Result:** 2 minutes to triage all projects, unblock work, access deliverable

**Without portfolio view:** User would need to open each project separately, unclear what needs attention.

---

### Scenario 2: Starting Multiple Projects

**User has 3 tasks to delegate:**

1. **From Portfolio Dashboard:**
   - Click "+ New Project"
   - Type: "Analyze Q4 sales data"
   - Agent asks clarifying questions (Hybrid Chat)
   - User provides files → Project starts

2. **Immediately start another:**
   - Click "+ New Project" again
   - Type: "Create competitor analysis report"
   - Agent starts → Project #2 running

3. **And another:**
   - Click "+ New Project"
   - Type: "Design new landing page mockups"
   - Agent starts → Project #3 running

**Portfolio shows all 3 running in parallel:**
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Q4 Sales    │ │ Competitor  │ │ Landing Pg  │
│ Analysis    │ │ Analysis    │ │ Mockups     │
│ Running 45% │ │ Running 20% │ │ Running 10% │
└─────────────┘ └─────────────┘ └─────────────┘
```

**User continues other work** while agents execute in parallel.

---

### Scenario 3: Context Switching

**User working in "Sales Analysis" project (Mission Control view):**

1. Notification appears: "Competitor Analysis complete"
2. User clicks notification → Portfolio Dashboard
3. Sees "Competitor Analysis" card with ✓ Complete status
4. Clicks card → Artifact opens (competitor report PDF)
5. User reviews report
6. Clicks "Back to Portfolio"
7. Resumes "Sales Analysis" → Mission Control view still in same state

**Seamless context switching** without losing place.

---

## Implementation Recommendations

### Phase 1: Portfolio Dashboard (MVP)

**Core features:**
- Card grid view for up to 6 projects
- Basic state indicators (Running, Complete, Needs Input)
- Click to drill into project (uses Delegation Desk view)
- Notification badges for attention-needed

**Timeline:** 2-3 weeks

---

### Phase 2: Multi-UX Paradigm Support

**Enhancements:**
- User can select which UX paradigm per project
- Portfolio routes to appropriate view on drill-down
- Projects remember their selected paradigm

**Timeline:** 3-4 weeks

---

### Phase 3: Advanced Multi-Project Features

**Additions:**
- Cross-project context sharing
- Resource allocation visualization
- Project templates and cloning
- Batch operations
- List view toggle for 7+ projects

**Timeline:** 4-6 weeks

---

## Open Questions

1. **How many concurrent projects is realistic?**
   - MVP: Support 1-6 projects
   - Scale goal: 50+ projects (need list view, search, filters)

2. **Should projects auto-archive after completion?**
   - Option A: Keep in "Active" for 7 days, then auto-archive
   - Option B: User manually archives
   - Hybrid: Auto-suggest archiving old completed projects

3. **How to handle project relationships/dependencies?**
   - Explicit linking (user says "Project B depends on Project A")
   - Auto-detection (agent sees Project A artifact, suggests using in Project B)
   - Visual indicators in portfolio (connecting lines between cards?)

4. **What happens when user has 20+ projects running?**
   - Pagination?
   - Infinite scroll?
   - Filters/search?
   - Priority-based visibility (hide low-priority background projects)?

---

## Conclusion

The mockup reveals a critical missing layer in our original 5 UX proposals: **multi-project orchestration**.

### Key Insights:

1. **Users work on multiple projects concurrently** - Portfolio dashboard essential
2. **State-appropriate presentation** - Show artifacts for complete work, not just logs
3. **Attention management** - Clear indicators when user action needed
4. **Context-appropriate UX** - Different projects may need different paradigms

### Recommendation:

**Build Proposal 6 (Portfolio Dashboard) as the entry point**, with routing to the most appropriate UX paradigm from our original 5 proposals based on project state and user preference.

**Architecture:**
```
Portfolio Dashboard (Meta-UX)
    │
    ├─ Simple projects → Delegation Desk (Proposal 2)
    ├─ Complex projects → Mission Control (Proposal 1)
    ├─ New users → Hybrid Chat (Proposal 5)
    └─ Audit-required → Timeline Narrative (Proposal 4)
```

This gives users the **best of all worlds**: high-level orchestration + deep-dive detail when needed.

---

**Next Steps:**
1. Prototype Portfolio Dashboard with 3-project mockup
2. Test routing to Delegation Desk (simplest paradigm)
3. Gather feedback on multi-project workflow
4. Expand to support other UX paradigms based on usage patterns
