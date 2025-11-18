# Autonomous Agent Web App - Implementation Plan

## Overview

Building a **delegation-focused web interface** for non-engineering users to interact with the Autonomous Agent P→E→V system.

## Technology Stack (Confirmed)

```
Frontend:      React 18 + TypeScript
UI Components: Shadcn/ui (Radix + Tailwind)
State:         Tanstack Query + Zustand
Routing:       React Router v6
Real-time:     Server-Sent Events (SSE)
Build Tool:    Vite
```

## Project Structure

```
web/
├── public/
├── src/
│   ├── components/
│   │   ├── ui/              # Shadcn components
│   │   ├── TaskDelegationForm.tsx
│   │   ├── ProgressPipeline.tsx
│   │   ├── TaskResults.tsx
│   │   ├── ArtifactCard.tsx
│   │   ├── VerificationBadge.tsx
│   │   └── TaskCard.tsx
│   ├── views/
│   │   ├── Dashboard.tsx
│   │   ├── TaskSubmit.tsx
│   │   ├── TaskProgress.tsx
│   │   ├── TaskResults.tsx
│   │   └── TaskFailure.tsx
│   ├── hooks/
│   │   ├── useTaskSubmit.ts
│   │   ├── useTaskProgress.ts
│   │   ├── useTaskResults.ts
│   │   └── useTaskHistory.ts
│   ├── api/
│   │   └── client.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── README.md
```

## MVP Features (Week 1-2)

### Priority 1: Core Delegation Flow
1. Task submission form
2. Progress monitor with SSE
3. Results display with download
4. Basic verification display

### Priority 2: Navigation & History
5. Task history dashboard
6. Status filtering
7. Retry failed tasks
8. Template reuse

## Key Design Principles

1. **Delegation-first** - Not a chat interface
2. **Artifact-centric** - Deliverables are the hero
3. **Trust through transparency** - Show verification
4. **Progressive disclosure** - Simple → powerful
5. **Mobile-first** - Touch-optimized

## API Integration

**Backend URL**: `http://localhost:8000`

**Endpoints**:
- POST `/tasks` - Submit task
- GET `/tasks/{id}` - Get status
- GET `/tasks/{id}/result` - Get result
- GET `/tasks/{id}/stream` (SSE) - Real-time updates

## Implementation Phases

### Phase 1: Setup (Day 1)
- Initialize Vite + React + TypeScript
- Install dependencies (Shadcn, Tanstack Query, React Router)
- Set up folder structure
- Configure Tailwind

### Phase 2: Core Components (Day 2-3)
- TaskDelegationForm
- ProgressPipeline
- TaskResults
- Verification Badge

### Phase 3: Views (Day 4-5)
- Dashboard (task history)
- TaskSubmit view
- TaskProgress view
- TaskResults view

### Phase 4: Integration (Day 6-7)
- API client setup
- Tanstack Query hooks
- SSE integration
- Routing logic

### Phase 5: Polish (Day 8-10)
- Mobile responsive
- Error handling
- Loading states
- Accessibility

## Success Criteria

- ✅ User can submit task in <5 clicks
- ✅ Progress updates in real-time
- ✅ Results downloadable immediately
- ✅ Verification clearly visible
- ✅ Mobile-friendly (works on phone)
- ✅ Accessible (WCAG AA)

## Next Steps

1. Initialize Vite project
2. Install dependencies
3. Set up Shadcn/ui
4. Build core components
5. Integrate with backend API

---

See [/ultrathink-task output] for complete UX/UI design specifications.
