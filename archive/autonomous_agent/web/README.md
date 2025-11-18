# Autonomous Agent Web UI

Production-quality React + TypeScript web application for the Autonomous Agent system.

## Features

- **Task Delegation**: Submit tasks with optional context and constraints
- **Real-time Progress**: Monitor task execution through planning, executing, and verification stages
- **Results Display**: View artifacts, verification checks, and download results
- **Task History**: Browse and filter past tasks by status
- **Mobile Responsive**: Works seamlessly on all devices

## Technology Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Tanstack Query** - API state management
- **React Router v6** - Client-side routing
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running at `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Copy environment template (optional - defaults to localhost:8000)
cp .env.example .env
```

### Development

```bash
# Start dev server (default: http://localhost:5173)
npm run dev
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── api/
│   └── client.ts          # API client with typed fetch wrappers
├── components/
│   ├── ProgressView.tsx   # Task progress monitor
│   ├── ResultsView.tsx    # Task results display
│   ├── TaskCard.tsx       # Task history card
│   └── TaskForm.tsx       # Task submission form
├── hooks/
│   └── useTasks.ts        # Tanstack Query hooks for tasks
├── types/
│   └── index.ts           # TypeScript type definitions
├── views/
│   ├── Dashboard.tsx      # Main dashboard view
│   └── TaskDetail.tsx     # Task detail view
├── App.tsx                # Main app with routing
├── main.tsx               # Entry point with providers
└── index.css              # Tailwind CSS imports
```

## API Integration

The app integrates with the backend API at `http://localhost:8000`:

- `POST /tasks` - Create new task
- `GET /tasks` - List all tasks
- `GET /tasks/{id}` - Get task details
- `GET /tasks/{id}/result` - Get task results
- `GET /tasks/{id}/artifacts/{path}` - Download artifact

## Design Philosophy

Following the **Ruthless Simplicity** principle:

- No unnecessary abstractions
- Direct API integration via Tanstack Query
- Simple polling (2s interval) for active tasks
- Tailwind utility classes (no custom CSS)
- Type-safe throughout
- Clear error messages

## Development Guidelines

1. **TypeScript Strict**: All code fully typed
2. **Error Handling**: User-friendly error messages
3. **Loading States**: Clear feedback on all async operations
4. **Mobile First**: Responsive design starting from mobile
5. **Accessibility**: Semantic HTML, proper ARIA labels

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

## Environment Variables

Create a `.env` file (optional):

```
VITE_API_URL=http://localhost:8000
```

Default: `http://localhost:8000`

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT
