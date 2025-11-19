# Outcomist Frontend

React + TypeScript + Vite frontend for Outcomist multi-project workspace.

## Setup

```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:3000
```

## Backend

Backend must be running at http://localhost:8000

## Architecture

- **React 18** with TypeScript
- **Vite** for build tooling
- **TailwindCSS** for styling
- **EventSource API** for SSE streaming
- **Custom hooks** for data fetching and state management

## Project Structure

```
src/
├── api/              # API client
├── hooks/            # React hooks
├── components/       # UI components
│   ├── workspace/    # Workspace-level components
│   └── project/      # Project card components
├── types/            # TypeScript types
└── styles/           # Global styles
```

## Features

- **Multi-project workspace** with grid layout
- **Real-time streaming** via SSE
- **Agent chat interface** with message history
- **Preview toggle** for viewing outputs
- **Session management** with tabs
- **Status indicators** for project state
- **Glassmorphism design** matching prototypes

## Development

- Backend proxy configured in `vite.config.ts`
- All API calls proxied to `http://localhost:8000`
- Hot reload enabled for rapid development
