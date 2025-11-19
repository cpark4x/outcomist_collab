# Outcomist Backend

Multi-project AI workspace backend built with FastAPI and Claude AI.

## Setup

### Prerequisites

- Python 3.11+
- Anthropic API key

### Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

## Architecture

### Directory Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database/            # Database models and connection
│   ├── api/                 # REST API endpoints
│   ├── services/            # Business logic
│   └── ai/                  # Claude AI integration
├── requirements.txt         # Python dependencies
└── pyproject.toml          # Project metadata
```

### Database

Uses SQLite with SQLAlchemy async ORM. Database file: `data/database.sqlite`

Models:
- `Project` - Projects with type (game, trip, content, presentation)
- `Session` - Conversation sessions within projects
- `Message` - Individual messages in conversations
- `File` - File attachments for projects/sessions

### API Endpoints

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

## Testing

### Manual API Testing

1. **Create a project:**
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "My Game", "description": "An adventure game", "type": "game"}'
```

2. **Create a session:**
```bash
curl -X POST http://localhost:8000/api/projects/{project_id}/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Design Session"}'
```

3. **Send a message:**
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Help me design a fantasy RPG"}'
```

### Using the API Docs

Open `http://localhost:8000/docs` for interactive API documentation where you can test all endpoints.

## Development

### Adding New Features

1. Add database models in `src/database/models.py`
2. Create service layer in `src/services/`
3. Add API endpoints in `src/api/`
4. Update router imports in `src/main.py`

### Environment Variables

- `ANTHROPIC_API_KEY` - Claude API key (required)
- `DATABASE_URL` - Database connection string
- `DATA_DIR` - Directory for project files
- `CLAUDE_MODEL` - Claude model to use (default: claude-3-5-sonnet-20241022)

## Next Steps (Future Phases)

- Phase 2: Add SSE streaming for real-time responses
- Phase 3: Build React frontend
- Phase 4: Add file upload/management
- Phase 5: Docker containerization
