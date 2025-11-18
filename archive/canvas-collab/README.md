# Canvas Collab

A canvas-based AI collaboration tool with infinite workspace, built with Electron, React, and TypeScript.

## Features

- **Infinite 2D Canvas**: Pan and zoom around a limitless workspace
- **Multiple Claude AI Agents**: Run multiple Claude instances simultaneously
- **Real-time Streaming**: See AI responses as they're generated
- **Persistent State**: All conversations and widget positions saved to SQLite
- **Drag & Drop**: Freely position widgets anywhere on the canvas
- **Resizable Widgets**: Adjust widget sizes to your preference

## Prerequisites

- Node.js 18+ or pnpm
- Anthropic API key

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## Development

Run in development mode:
```bash
npm run electron:dev
```

This will start both the Vite dev server and Electron app with hot reload.

## Build

Build for production:
```bash
npm run electron:build
```

## Usage

1. Click "+ New Agent" to create a new Claude AI widget
2. Type your message and press Enter or click Send
3. Drag widgets by their header to reposition
4. Resize widgets by dragging the bottom-right corner
5. Use mouse wheel to pan (or Shift+drag)
6. Use Ctrl/Cmd+wheel to zoom

## Architecture

- **Main Process** (`src/main/`): Electron main process, handles IPC, database, and AI
- **Preload** (`src/preload/`): Security boundary for IPC communication
- **Renderer** (`src/renderer/`): React UI with Canvas and widgets
- **Database**: SQLite for workspace and conversation persistence

## Next Steps

- [ ] Add tool execution (bash, file operations, web search)
- [ ] Implement widget spawning from Claude
- [ ] Add document editor widget
- [ ] Add file browser widget
- [ ] Implement conversation history
- [ ] Add workspace management UI

## License

MIT
