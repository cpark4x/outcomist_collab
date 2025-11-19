# Quick Start Guide

## Phase 1: Backend Foundation

This guide will help you get the Outcomist backend up and running quickly.

## Prerequisites

- Python 3.11 or higher
- Anthropic API key (for Claude AI integration)

## Setup Steps

### 1. Install Dependencies

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-...your-key-here
```

### 3. Test Database Operations (No API Key Required)

```bash
python test_api.py
```

This will:
- Initialize the SQLite database
- Create test projects and sessions
- Store test messages
- Verify all CRUD operations work

Expected output:
```
=== Testing Database Operations ===

1. Initializing database...
   ✓ Database initialized

2. Creating a project...
   ✓ Created project: <uuid>
   ...

=== All Tests Passed! ===
```

### 4. Start the Server

```bash
uvicorn src.main:app --reload
```

The server will start at `http://localhost:8000`

### 5. Verify API

Open your browser to:
- API Root: `http://localhost:8000/`
- API Docs: `http://localhost:8000/docs` (interactive Swagger UI)
- Health Check: `http://localhost:8000/health`

## Testing the API

### Using the Interactive Docs

1. Go to `http://localhost:8000/docs`
2. Try the following sequence:

**Create a Project:**
```json
POST /api/projects
{
  "name": "My Fantasy Game",
  "description": "An epic adventure",
  "type": "game"
}
```

**Create a Session:**
```json
POST /api/projects/{project_id}/sessions
{
  "name": "Design Session"
}
```

**Send a Message (Requires API Key):**
```json
POST /api/sessions/{session_id}/messages
{
  "content": "Help me design a fantasy RPG with magic and combat"
}
```

### Using cURL

```bash
# Create a project
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"My Game","description":"Adventure game","type":"game"}'

# Get all projects
curl http://localhost:8000/api/projects

# Create a session (replace {project_id})
curl -X POST http://localhost:8000/api/projects/{project_id}/sessions \
  -H "Content-Type: application/json" \
  -d '{"name":"Design Session"}'

# Send a message (replace {session_id}, requires API key)
curl -X POST http://localhost:8000/api/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"content":"Help me design a fantasy RPG"}'
```

## What's Working

✅ **Database Models** - Projects, Sessions, Messages, Files
✅ **Project CRUD** - Create, read, update, delete projects
✅ **Session CRUD** - Create and manage conversation sessions
✅ **Message Storage** - Store and retrieve conversation history
✅ **Claude AI Integration** - Send messages and get AI responses
✅ **Type Safety** - Full type hints and Pydantic validation
✅ **Auto Documentation** - Swagger UI at /docs

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings (API keys, DB config)
│   ├── database/
│   │   ├── models.py        # SQLAlchemy models
│   │   └── connection.py    # Database setup
│   ├── api/
│   │   ├── projects.py      # Project endpoints
│   │   ├── sessions.py      # Session endpoints
│   │   └── messages.py      # Message endpoints
│   ├── services/
│   │   ├── project_service.py
│   │   ├── session_service.py
│   │   └── message_service.py
│   └── ai/
│       ├── agent.py         # Claude API client
│       └── prompts.py       # System prompts by project type
├── data/
│   ├── projects/            # Generated project files
│   └── database.sqlite      # SQLite database
└── test_api.py              # Test script
```

## Next Steps

- **Phase 2**: Add SSE streaming for real-time AI responses
- **Phase 3**: Build React frontend
- **Phase 4**: Add file upload/management
- **Phase 5**: Docker containerization

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
rm data/database.sqlite
python test_api.py
```

### Port Already in Use

If port 8000 is busy:
```bash
uvicorn src.main:app --reload --port 8001
```

### Import Errors

Make sure you're in the activated virtual environment:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

## API Documentation

Full API documentation is available at `http://localhost:8000/docs` when the server is running.

### Available Endpoints

**Projects**
- `POST /api/projects` - Create project
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

**Sessions**
- `POST /api/projects/{project_id}/sessions` - Create session
- `GET /api/projects/{project_id}/sessions` - List sessions
- `GET /api/sessions/{id}` - Get session

**Messages**
- `POST /api/sessions/{id}/messages` - Send message, get AI response
- `GET /api/sessions/{id}/messages` - Get conversation history

## Support

For issues or questions, refer to the main README.md or check the `/docs` endpoint for API details.
