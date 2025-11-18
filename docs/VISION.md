# Outcomist - Project Vision

## What is Outcomist?

Outcomist is a Claude-powered creative workspace where you can build games, plan trips, create content, and design presentations through natural conversation. It's designed to make AI-assisted creation feel effortless and collaborative.

## Core Vision

**"Claude as your creative partner"** - We believe AI should amplify human creativity, not replace it. Outcomist provides a canvas where ideas become reality through conversation, with Claude handling the technical implementation while you focus on the creative vision.

## Current Status (November 2025)

### ✅ What's Working

**Core Features**:
- Multi-project workspace with visual project cards
- Real-time chat with Claude AI
- Live preview of generated content (HTML/CSS/JS)
- File management system with MIME type support
- Project-specific AI context (Game, Trip, Content, Presentation)
- Auto-bundling of CSS/JS into preview HTML
- Auto-naming of projects based on first user message
- Session management (auto-hide tabs when single session)

**Technical Implementation**:
- FastAPI async backend with SQLite database
- React TypeScript frontend with Vite
- Server-Sent Events (SSE) for streaming responses
- Claude 3.5 Sonnet integration via Anthropic SDK
- File storage and retrieval system
- Multi-tool support (create_file, update_project_name)

### 🚧 In Progress

- Running status indicator (visual feedback during AI processing)
- Session deletion (backend endpoint needed)
- Better error handling and user feedback

### 📋 Planned Features

**Near-term**:
- Export/download project files
- Project templates and examples
- Improved mobile responsiveness
- Dark mode support
- Collaborative editing (multiple users per project)

**Future Vision**:
- Version control for generated files
- Asset library integration (images, icons, fonts)
- AI-powered debugging and optimization
- Integration with external services (deployment, hosting)
- Plugin system for custom tools and capabilities

## Design Philosophy

1. **Conversation-first** - Natural language is the primary interface
2. **Live preview** - See results instantly as they're created
3. **Context-aware** - Claude understands what you're building
4. **File-based** - Everything is a file that can be edited and managed
5. **Project-scoped** - Each project has its own isolated workspace

## Success Metrics

We'll know we're successful when:
- Users create complete projects in a single session
- First-time users ship something within 10 minutes
- Users return to iterate on previous projects
- The preview "just works" without manual file linking
- Users feel like they're collaborating with Claude, not commanding it

## Technical Principles

1. **Keep it simple** - Avoid over-engineering; ship working features
2. **Real-time first** - Streaming responses, live updates
3. **AI-native** - Design around what AI does well
4. **Files as first-class citizens** - Everything is visible and editable
5. **Progressive enhancement** - Start basic, add polish incrementally

## Open Questions

- How do we handle complex multi-file projects (e.g., React apps)?
- Should we support version control / project history?
- What's the right balance between AI autonomy and user control?
- How do we make collaboration work (sharing, forking, remixing)?

## References

- Product Specification: [docs/specs/](./specs/)
- Planning Documents: [docs/planning/](./planning/)
- Design Mockups: [docs/design-mockups/](./design-mockups/)
- Application Code: [outcomist/](../outcomist/)

---

**Last Updated**: November 17, 2025
