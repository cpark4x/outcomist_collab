# Canvas UI - Visual Workspace for Autonomous Agent

## 🎨 What is Canvas UI?

The Canvas UI is a **visual, spatial workspace** where tasks appear as draggable cards on an infinite canvas. Think Figma meets task management - a more interactive, visual way to work with your autonomous agent.

## ✨ Key Features

### 1. Spatial Organization
- Tasks appear as cards anywhere on the canvas
- Drag and drop to organize your workspace
- Create a visual map of your work

### 2. Real-time Updates
- Watch tasks progress live
- Cards update with current status
- Artifacts appear as they're generated

### 3. Expandable Cards
- Collapsed view: See status at a glance
- Expanded view: Full details, artifacts, verification

### 4. Persistent Workspace
- Canvas state saved to browser
- Return to your workspace anytime
- No data lost on refresh

## 🚀 How to Use

### Access the Canvas

Open: **http://localhost:5173**

The canvas is now the default homepage.

**Old dashboard**: http://localhost:5173/dashboard

### Create Your First Task

1. **Click "New Task"** button (top right)
2. **Enter your goal** in the modal
3. **Click "Create Task"**
4. **Watch the card appear** on the canvas

### Interact with Task Cards

**Drag to move**:
- Click and drag the card anywhere
- Organize tasks spatially

**Expand/Collapse**:
- Click the maximize/minimize icon
- See full details or save space

**Download artifacts**:
- Expanded view shows artifacts
- Click download icon on each artifact

**Remove tasks**:
- Click the X icon
- Clears from canvas (doesn't delete from backend)

### Task Card States

Cards change appearance based on status:

**🔵 Blue border** = Running (planning/executing/verifying)
**🟢 Green border** = Completed successfully
**🔴 Red border** = Failed
**⚪ Gray border** = Pending

### Organize Your Workspace

**By project**: Group related tasks together
**By status**: Completed tasks in one area, running in another
**By user**: If multiple people use it, each gets their space
**By time**: Today's tasks here, this week's there

## 🎯 Use Cases

### 1. Multi-Task Workflow
Create multiple tasks and watch them all progress:
```
[Task 1: Research]  [Task 2: Analysis]  [Task 3: Report]
       ↓                   ↓                   ↓
   Complete          In Progress           Pending
```

### 2. Comparison View
Run similar tasks side-by-side:
```
[Approach A]    vs    [Approach B]
```

### 3. Pipeline Visualization
See your data pipeline spatially:
```
[Collect Data] → [Process] → [Analyze] → [Report]
```

### 4. Workspace Persistence
Your canvas survives page refresh - organize once, use forever.

## 🎨 Visual Design

### Color Scheme
- **Background**: Dark gradient (slate-900 → slate-800)
- **Grid pattern**: Subtle 50px grid
- **Cards**: Semi-transparent with colored borders
- **Status colors**: Blue (active), Green (success), Red (failure)

### Animations
- **Card drag**: Smooth position updates
- **Progress spinner**: Animated on running tasks
- **Progress bar**: Animated verification confidence
- **Hover effects**: Subtle shadows and color shifts

### Typography
- **Card title**: Status (Completed, Running, etc.)
- **Task ID**: First 8 characters for reference
- **Progress text**: Current step being executed
- **Artifact names**: Full filename

## 🔄 Canvas vs Dashboard

### Canvas (New Default)

**Best for**:
- Visual thinkers
- Multi-tasking workflows
- Spatial organization
- Real-time monitoring
- Comparing multiple tasks

**Feels like**:
- Figma canvas
- Notion board view
- Physical desk with papers

### Dashboard (Original)

**Best for**:
- List-oriented thinking
- Historical review
- Filtering by status
- Linear workflows
- Traditional task management

**Feels like**:
- Gmail inbox
- Linear issues
- Traditional project management

**Access**: http://localhost:5173/dashboard

## 💡 Tips & Tricks

### 1. Organize as You Go
Don't wait until it's messy - organize tasks as you create them.

### 2. Use Space Generously
The canvas is infinite - spread out, don't clutter.

### 3. Create Visual Patterns
- Top row = Today's tasks
- Left column = High priority
- Right side = Completed
- Bottom = Reference/archived

### 4. Collapse When Done
Collapse completed tasks to save screen space but keep them visible.

### 5. Quick Access
Bookmark canvas for quick access: `http://localhost:5173`

## 🎭 Example Workflows

### Workflow 1: Content Creation Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Research   │ →  │   Draft     │ →  │   Polish    │
│   Topics    │    │  Outline    │    │   Final     │
└─────────────┘    └─────────────┘    └─────────────┘
     ✓                  ⟳                   ○
```

### Workflow 2: Competitive Analysis

```
┌─────────────┐    ┌─────────────┐
│  Company A  │    │  Company B  │
│  Analysis   │    │  Analysis   │
└─────────────┘    └─────────────┘
       ↓                  ↓
┌──────────────────────────────────┐
│    Comparison Report             │
│    (waits for both to complete)  │
└──────────────────────────────────┘
```

### Workflow 3: Iterative Refinement

```
Version 1 → Version 2 → Version 3
  (done)      (done)    (running)

Each card shows the evolution
```

## 🔧 Technical Details

### State Management
- **React useState**: Local component state
- **LocalStorage**: Persists canvas layout
- **Polling**: 2-second intervals for task updates

### Data Flow
```
User creates task
  ↓
POST /tasks (backend)
  ↓
Card appears on canvas
  ↓
Poll GET /tasks/{id} every 2s
  ↓
Card updates in real-time
  ↓
Fetch result when complete
  ↓
Show artifacts + verification
```

### Browser Storage
```javascript
localStorage.setItem('canvas-tasks', JSON.stringify(tasks))
// Stores: task ID, position, expanded state
```

## 🐛 Troubleshooting

### Cards Not Updating
**Issue**: Tasks frozen, no progress
**Fix**: Check backend is running (http://localhost:8000)

### Can't Drag Cards
**Issue**: Drag doesn't work
**Fix**: Refresh page, clear localStorage

### Artifacts Not Downloading
**Issue**: Download button doesn't work
**Fix**: Check browser console, backend logs

### Cards Disappear on Refresh
**Issue**: Canvas resets
**Fix**: localStorage might be disabled - check browser settings

## 🎨 Customization Ideas

### Future Enhancements

**Visual connections**:
- Draw arrows between related tasks
- Show dependencies visually

**Custom card colors**:
- Tag tasks with colors
- Filter by color

**Zoom controls**:
- Zoom in/out of canvas
- Fit all tasks in view

**Minimap**:
- Overview of full canvas
- Quick navigation

**Collaboration**:
- See others' cursors
- Real-time shared canvas

**Templates**:
- Save canvas layouts
- Load pre-organized workspaces

## 📊 Comparison: Canvas vs Chat vs Form

| Feature | Canvas | Chat | Form |
|---------|--------|------|------|
| Visual | ✅ Spatial | ❌ Linear | ⚠️ Single |
| Multi-task | ✅ Parallel | ⚠️ Sequential | ❌ One at a time |
| Organization | ✅ Drag & drop | ❌ Chronological | ❌ List only |
| Real-time | ✅ All visible | ⚠️ Scroll to find | ⚠️ Single view |
| Delegation feel | ✅ Workspace | ⚠️ Conversation | ✅ Task assignment |
| Monitoring | ✅ At a glance | ❌ Must ask | ⚠️ Dashboard needed |

## 🎯 Best Practices

### Do
- ✅ Organize tasks spatially
- ✅ Use collapse/expand strategically
- ✅ Remove completed tasks regularly
- ✅ Create new tasks freely

### Don't
- ❌ Overcrowd one area
- ❌ Keep 100+ tasks on canvas
- ❌ Forget to download artifacts before removing
- ❌ Drag cards off-screen

## 🚀 Getting Started Checklist

- [ ] Open http://localhost:5173
- [ ] Create your first task
- [ ] Watch it progress in real-time
- [ ] Drag the card to a new position
- [ ] Expand/collapse the card
- [ ] Download an artifact
- [ ] Create a second task
- [ ] Organize both tasks spatially
- [ ] Refresh page (canvas persists!)
- [ ] Remove a task when done

## 🎉 You're Ready!

The Canvas UI gives you a **visual, spatial workspace** for delegating work to your autonomous agent. It's perfect for **visual thinkers**, **multi-tasking workflows**, and anyone who wants to see their work laid out spatially.

**Start creating**: http://localhost:5173

---

*Canvas UI - Where delegation meets spatial organization*
