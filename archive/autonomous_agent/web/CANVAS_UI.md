# Canvas UI for Autonomous Agent

A complete widget-based Canvas workspace adapted from canvas-ai for the autonomous agent system.

## Features

### Widget System
- **Draggable & Resizable**: Click and drag widgets to reposition, resize from corners/edges in expanded mode
- **Three States**:
  - **Expanded**: Full view with logs and artifacts
  - **Compact**: Minimal view with summary
  - **Minimized**: Title bar only
- **Status Indicators**: Visual status with colored indicators (idle, running, completed, error)
- **Z-Index Management**: Click to bring widgets to front

### Task Integration
- **Auto-submission**: Creating a widget automatically submits a task to the backend
- **Real-time polling**: Task status updates every 2 seconds
- **Progress tracking**: Backend progress messages stream into logs
- **Artifact downloads**: Download completed task artifacts with one click
- **Verification display**: Shows confidence scores for completed tasks

### Canvas Controls
- **Pan**: Shift+drag or middle-mouse drag to pan the canvas
- **Zoom**: Ctrl/Cmd+scroll to zoom in/out, toolbar buttons for zoom control
- **Grid Background**: Visual grid for positioning reference
- **Persistent Layout**: Widget positions and states saved to localStorage

## Usage

### Starting the Application

1. **Backend**: Make sure the FastAPI backend is running on port 8000
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**: Start the dev server
   ```bash
   cd web
   npm run dev
   ```

3. **Access**: Open http://localhost:5173

### Creating a Task

1. Click **"New Task"** button in the toolbar
2. Enter your task goal in natural language
3. Click **"Create Task"**
4. A new widget appears and task is automatically submitted to backend

### Widget Interactions

**Dragging**:
- Click and hold the widget header
- Move mouse to reposition
- Release to drop in new position

**Resizing** (expanded mode only):
- Hover over widget edges/corners
- Click and drag resize handles
- Works from all 8 directions (n, ne, e, se, s, sw, w, nw)

**State Changes**:
- Click minimize button (−) for compact view
- Click maximize button (□) for expanded view
- Double-click header to toggle between expanded/compact
- Click X to close widget

**Selecting**:
- Click widget to select (shows colored glow on status indicator)
- Click canvas background to deselect all

### Status Indicators

- **Gray**: Idle - waiting to start
- **Blue** (pulsing): Running - task in progress
- **Amber**: Paused - task paused
- **Green**: Completed - task finished successfully
- **Red**: Error - task failed

### Log Viewer

- **Auto-scroll**: Automatically scrolls to newest logs
- **Manual scroll**: Scroll up to view history (disables auto-scroll)
- **Scroll to bottom**: Button appears when not at bottom
- **Timestamps**: Shows when each log entry occurred
- **Log levels**: Color-coded by level (info, warn, error, success)

### Artifacts

When task completes:
- **Artifacts section** appears below logs
- Click download button to save artifact
- Shows file name and type
- Downloads as JSON file

### Verification

- **Progress bar** shows task confidence level
- **Percentage** displays exact confidence score
- **Green gradient** indicates successful verification

## Canvas Navigation

### Panning
- **Shift + drag**: Pan while holding shift key
- **Middle-mouse drag**: Pan with middle mouse button
- **Trackpad**: Two-finger swipe (when not on widget)

### Zooming
- **Ctrl/Cmd + scroll**: Zoom in/out
- **Toolbar buttons**: Use +/- buttons
- **Reset**: Click "Reset" to return to 100% zoom and center position

## Keyboard Shortcuts

- **Shift + drag**: Pan canvas
- **Ctrl/Cmd + scroll**: Zoom in/out
- **Double-click header**: Toggle widget state
- **Escape**: Deselect all widgets (future)

## Architecture

### Components

**AgentWidget** (`src/components/AgentWidget.tsx`):
- Main widget container
- Handles dragging, resizing, task polling
- Manages widget lifecycle

**WidgetHeader** (`src/components/WidgetHeader.tsx`):
- Title bar with status indicator
- State controls (minimize, maximize, close)
- Rename functionality (double-click title)

**WidgetBody** (`src/components/WidgetBody.tsx`):
- Adaptive content based on widget state
- Shows logs, artifacts, verification
- Handles different view modes

**LogViewer** (`src/components/LogViewer.tsx`):
- Auto-scrolling log display
- Colored log levels
- Scroll-to-bottom button

**Canvas** (`src/views/Canvas.tsx`):
- Main workspace container
- Toolbar and controls
- Widget management
- Pan/zoom functionality

### State Management

**useCanvasState** (`src/hooks/useCanvasState.ts`):
- Manages all widgets in a Map
- Handles selection and z-index
- Provides update, add, remove operations
- Serialization for localStorage

### Backend Integration

**API Client** (`src/api/client.ts`):
- Typed fetch wrappers
- Task creation, status polling, result fetching
- Artifact downloads

**Polling Strategy**:
- Every 2 seconds while task is running
- Stops when task completes or fails
- Updates widget logs with progress messages
- Fetches result and artifacts on completion

## Customization

### Widget Colors

Status colors defined in `src/types/widget.ts`:
```typescript
export const STATUS_COLORS: Record<AgentStatus, string> = {
  idle: '#6B7280',      // Gray
  running: '#3B82F6',   // Blue
  paused: '#F59E0B',    // Amber
  error: '#EF4444',     // Red
  completed: '#10B981', // Green
};
```

### Widget Sizes

Default sizes in `src/types/widget.ts`:
```typescript
export const DEFAULT_WIDGET_CONFIG: WidgetConfig = {
  minWidth: 200,
  minHeight: 100,
  maxWidth: 800,
  maxHeight: 600,
  expandedWidth: 600,
  expandedHeight: 500,
  compactWidth: 300,
  compactHeight: 150,
  minimizedWidth: 200,
  minimizedHeight: 60,
};
```

## Development

### Adding New Widget Types

1. Add type to `WidgetType` in `src/types/widget.ts`
2. Update `AgentWidgetData` interface with type-specific fields
3. Create component for new widget body
4. Update `AgentWidget` to render new type
5. Add creation function in Canvas

### Extending Task Features

- Task cancellation: Add stop button and backend integration
- Task history: Store completed tasks in database
- Task templates: Pre-defined task configurations
- Task chains: Link dependent tasks together

## Troubleshooting

**Widgets not updating**:
- Check backend is running on port 8000
- Check browser console for API errors
- Verify CORS is enabled in backend

**Dragging doesn't work**:
- Make sure you're clicking widget header, not body
- Check for JavaScript errors in console

**Logs not showing**:
- Verify backend is sending progress updates
- Check task polling is active (every 2s)
- Look for errors in task status endpoint

**Layout not saving**:
- Check localStorage is enabled
- Clear localStorage and reload if corrupted
- Verify serialization in browser DevTools

## Future Enhancements

- Keyboard shortcuts for all actions
- Widget relationships (connect related tasks)
- Auto-arrange widgets (grid layout)
- Export/import layouts
- Multi-select widgets
- Copy/paste widgets
- Undo/redo canvas actions
- Mini-map for canvas navigation
- Search/filter widgets
- Widget templates
- Collaboration features
