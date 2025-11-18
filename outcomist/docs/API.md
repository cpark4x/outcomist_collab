# API Documentation

Complete API reference for the Outcomist backend.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication is required. This is an MVP.

**Production considerations:**
- Add JWT or session-based auth
- API key per user
- Rate limiting
- OAuth integration

## Table of Contents

- [Projects](#projects)
- [Sessions](#sessions)
- [Messages](#messages)
- [Files](#files)
- [Streaming](#streaming)
- [Health Check](#health-check)
- [Error Responses](#error-responses)

## Projects

### List Projects

Get all projects for the user.

```http
GET /api/projects
```

**Response:**
```json
{
  "projects": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "name": "My Game Project",
      "description": "A simple platformer game",
      "type": "game",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T14:45:00Z"
    }
  ]
}
```

**cURL:**
```bash
curl http://localhost:8000/api/projects
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/projects');
const data = await response.json();
```

### Create Project

Create a new project.

```http
POST /api/projects
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Trip to Paris",
  "description": "7-day family vacation",
  "type": "trip"
}
```

**Fields:**
- `name` (string, required) - Project name (1-100 characters)
- `description` (string, required) - Project description (1-500 characters)
- `type` (string, required) - One of: "game", "trip", "content", "presentation"

**Response:**
```json
{
  "id": "01234567-89ab-cdef-0123-456789abcdef",
  "name": "Trip to Paris",
  "description": "7-day family vacation",
  "type": "trip",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Trip to Paris",
    "description": "7-day family vacation",
    "type": "trip"
  }'
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/projects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Trip to Paris',
    description: '7-day family vacation',
    type: 'trip'
  })
});
const project = await response.json();
```

### Get Project

Get a single project by ID.

```http
GET /api/projects/{project_id}
```

**Response:**
```json
{
  "id": "01234567-89ab-cdef-0123-456789abcdef",
  "name": "Trip to Paris",
  "description": "7-day family vacation",
  "type": "trip",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl http://localhost:8000/api/projects/01234567-89ab-cdef-0123-456789abcdef
```

### Update Project

Update a project.

```http
PUT /api/projects/{project_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "id": "01234567-89ab-cdef-0123-456789abcdef",
  "name": "Updated Project Name",
  "description": "Updated description",
  "type": "trip",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T15:00:00Z"
}
```

### Delete Project

Delete a project and all associated data.

```http
DELETE /api/projects/{project_id}
```

**Response:**
```json
{
  "message": "Project deleted successfully"
}
```

**Note:** This also deletes:
- All sessions for this project
- All messages in those sessions
- All files for this project
- Project directory on disk

## Sessions

### List Sessions

Get all sessions for a project.

```http
GET /api/projects/{project_id}/sessions
```

**Response:**
```json
{
  "sessions": [
    {
      "id": "session-uuid",
      "project_id": "project-uuid",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T14:45:00Z"
    }
  ]
}
```

### Create Session

Create a new session for a project.

```http
POST /api/projects/{project_id}/sessions
```

**Response:**
```json
{
  "id": "session-uuid",
  "project_id": "project-uuid",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Note:** Sessions are automatically created when a project is created.

### Get Session

Get a single session by ID.

```http
GET /api/sessions/{session_id}
```

**Response:**
```json
{
  "id": "session-uuid",
  "project_id": "project-uuid",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T14:45:00Z"
}
```

## Messages

### List Messages

Get all messages in a session.

```http
GET /api/sessions/{session_id}/messages
```

**Response:**
```json
{
  "messages": [
    {
      "id": "message-uuid",
      "session_id": "session-uuid",
      "role": "user",
      "content": "Create a simple game",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "message-uuid-2",
      "session_id": "session-uuid",
      "role": "assistant",
      "content": "I'll create a game for you...",
      "created_at": "2024-01-15T10:30:15Z"
    }
  ]
}
```

**Message roles:**
- `user` - Messages from the user
- `assistant` - Messages from AI
- `system` - System-generated messages (file creation notifications)

### Send Message (Streaming)

Send a message and receive streaming response via SSE.

```http
POST /api/sessions/{session_id}/messages/stream
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Create a simple platformer game"
}
```

**Response:** Server-Sent Events stream (see [Streaming](#streaming) section)

**cURL:**
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/messages/stream \
  -H "Content-Type: application/json" \
  -d '{"content": "Create a simple game"}' \
  -N
```

**JavaScript (using EventSource):**
```javascript
// First, send the message
const response = await fetch(
  `http://localhost:8000/api/sessions/${sessionId}/messages/stream`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: 'Create a simple game' })
  }
);

// Then connect to SSE stream
const eventSource = new EventSource(
  `http://localhost:8000/api/sessions/${sessionId}/stream`
);

eventSource.addEventListener('message_start', (e) => {
  const data = JSON.parse(e.data);
  console.log('Message started:', data.message_id);
});

eventSource.addEventListener('content_block_delta', (e) => {
  const data = JSON.parse(e.data);
  console.log('Content:', data.delta.text);
});

eventSource.addEventListener('message_stop', (e) => {
  console.log('Message complete');
  eventSource.close();
});

eventSource.addEventListener('error', (e) => {
  console.error('Stream error:', e);
  eventSource.close();
});
```

## Files

### List Files

Get all files for a project.

```http
GET /api/projects/{project_id}/files
```

**Response:**
```json
{
  "files": [
    {
      "id": "file-uuid",
      "project_id": "project-uuid",
      "filename": "index.html",
      "content": "<!DOCTYPE html>...",
      "created_at": "2024-01-15T10:35:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    },
    {
      "id": "file-uuid-2",
      "project_id": "project-uuid",
      "filename": "game.js",
      "content": "const canvas = document.getElementById...",
      "created_at": "2024-01-15T10:35:10Z",
      "updated_at": "2024-01-15T10:35:10Z"
    }
  ]
}
```

**cURL:**
```bash
curl http://localhost:8000/api/projects/{project_id}/files
```

**JavaScript:**
```javascript
const response = await fetch(
  `http://localhost:8000/api/projects/${projectId}/files`
);
const data = await response.json();
```

### Get File

Get a single file by ID.

```http
GET /api/files/{file_id}
```

**Response:**
```json
{
  "id": "file-uuid",
  "project_id": "project-uuid",
  "filename": "index.html",
  "content": "<!DOCTYPE html>...",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

### Create File

Create a new file (typically done by AI, but available for manual use).

```http
POST /api/projects/{project_id}/files
Content-Type: application/json
```

**Request Body:**
```json
{
  "filename": "script.js",
  "content": "console.log('Hello, world!');"
}
```

**Response:**
```json
{
  "id": "file-uuid",
  "project_id": "project-uuid",
  "filename": "script.js",
  "content": "console.log('Hello, world!');",
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": "2024-01-15T10:40:00Z"
}
```

### Update File

Update an existing file.

```http
PUT /api/files/{file_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "console.log('Updated content');"
}
```

**Response:**
```json
{
  "id": "file-uuid",
  "project_id": "project-uuid",
  "filename": "script.js",
  "content": "console.log('Updated content');",
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": "2024-01-15T10:45:00Z"
}
```

### Delete File

Delete a file.

```http
DELETE /api/files/{file_id}
```

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

## Streaming

### SSE Event Stream

Connect to receive real-time updates for a session.

```http
GET /api/sessions/{session_id}/stream
```

**Connection:**
```javascript
const eventSource = new EventSource(
  `http://localhost:8000/api/sessions/${sessionId}/stream`
);
```

### Event Types

#### message_start

Sent when a new AI message begins.

```json
{
  "type": "message_start",
  "message_id": "msg-uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### content_block_delta

Sent for each chunk of AI response text.

```json
{
  "type": "content_block_delta",
  "delta": {
    "type": "text_delta",
    "text": "I'll create a "
  }
}
```

**Note:** Multiple events will be sent as the AI generates response.

#### message_stop

Sent when the AI message is complete.

```json
{
  "type": "message_stop",
  "message_id": "msg-uuid",
  "timestamp": "2024-01-15T10:30:15Z"
}
```

#### file_created

Sent when AI creates a new file.

```json
{
  "type": "file_created",
  "file": {
    "id": "file-uuid",
    "filename": "index.html",
    "project_id": "project-uuid"
  }
}
```

#### file_updated

Sent when AI updates an existing file.

```json
{
  "type": "file_updated",
  "file": {
    "id": "file-uuid",
    "filename": "index.html",
    "project_id": "project-uuid"
  }
}
```

#### error

Sent when an error occurs.

```json
{
  "type": "error",
  "error": {
    "message": "Rate limit exceeded",
    "code": "rate_limit_error"
  }
}
```

### Complete Example

```javascript
const sessionId = 'your-session-id';

// 1. Send a message
await fetch(`http://localhost:8000/api/sessions/${sessionId}/messages/stream`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ content: 'Create a simple game' })
});

// 2. Connect to stream
const eventSource = new EventSource(
  `http://localhost:8000/api/sessions/${sessionId}/stream`
);

let currentMessageId = null;
let accumulatedContent = '';

// 3. Handle events
eventSource.addEventListener('message_start', (e) => {
  const data = JSON.parse(e.data);
  currentMessageId = data.message_id;
  accumulatedContent = '';
  console.log('AI started responding');
});

eventSource.addEventListener('content_block_delta', (e) => {
  const data = JSON.parse(e.data);
  accumulatedContent += data.delta.text;

  // Update UI with accumulated content
  document.getElementById('ai-response').textContent = accumulatedContent;
});

eventSource.addEventListener('message_stop', (e) => {
  console.log('AI finished responding');
  console.log('Complete message:', accumulatedContent);
});

eventSource.addEventListener('file_created', (e) => {
  const data = JSON.parse(e.data);
  console.log('File created:', data.file.filename);

  // Refresh file list in UI
  refreshFileList();
});

eventSource.addEventListener('error', (e) => {
  const data = JSON.parse(e.data);
  console.error('Error:', data.error.message);
  eventSource.close();
});
```

## Health Check

### Check Service Health

Verify the backend is running.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl http://localhost:8000/health
```

**Use cases:**
- Docker health checks
- Load balancer health probes
- Monitoring systems
- Deployment verification

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Common Errors

#### Invalid Project Type

```http
POST /api/projects
```

```json
{
  "name": "My Project",
  "description": "A project",
  "type": "invalid_type"
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "Invalid project type. Must be one of: game, trip, content, presentation"
}
```

#### Project Not Found

```http
GET /api/projects/nonexistent-id
```

**Response: 404 Not Found**
```json
{
  "detail": "Project not found"
}
```

#### Missing Required Fields

```http
POST /api/projects
```

```json
{
  "name": "My Project"
  // Missing description and type
}
```

**Response: 422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "loc": ["body", "description"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "type"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### API Key Not Configured

**Response: 500 Internal Server Error**
```json
{
  "detail": "ANTHROPIC_API_KEY not configured"
}
```

**Fix:** Add `ANTHROPIC_API_KEY` to backend `.env` file

#### Rate Limit Exceeded

**Response: 429 Too Many Requests** (from Anthropic API)
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

**Fix:** Wait a few minutes or upgrade Anthropic API plan

## Rate Limiting

Current MVP has no rate limiting on the Outcomist API.

**Anthropic API limits:**
- Depends on your API plan
- Typically 50-100 requests/minute
- Errors are passed through to client

**Production recommendations:**
- Add rate limiting per user/IP
- Implement exponential backoff
- Queue requests during high load
- Cache responses when appropriate

## CORS Configuration

Current CORS settings allow all origins (development mode).

**Development:**
```python
# backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production recommendations:**
```python
# Allow only your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

## API Versioning

Current API has no versioning (MVP).

**Future considerations:**
- `/api/v1/projects`
- `/api/v2/projects`
- Header-based versioning: `Accept: application/vnd.outcomist.v1+json`

## WebSocket Alternative

Current implementation uses SSE for simplicity.

**SSE vs WebSocket:**
- SSE: Server → Client only, simpler, works with standard HTTP
- WebSocket: Bidirectional, more complex, requires WS protocol

**When to consider WebSocket:**
- Need client → server streaming
- Very high message frequency
- Bidirectional communication required

## Example Client Library (Concept)

```javascript
class OutcomistClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async createProject(name, description, type) {
    const response = await fetch(`${this.baseUrl}/api/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description, type })
    });
    return await response.json();
  }

  async sendMessage(sessionId, content, onChunk, onComplete) {
    // Send message
    await fetch(`${this.baseUrl}/api/sessions/${sessionId}/messages/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });

    // Listen for response
    const eventSource = new EventSource(
      `${this.baseUrl}/api/sessions/${sessionId}/stream`
    );

    let accumulated = '';

    eventSource.addEventListener('content_block_delta', (e) => {
      const data = JSON.parse(e.data);
      accumulated += data.delta.text;
      onChunk(data.delta.text, accumulated);
    });

    eventSource.addEventListener('message_stop', () => {
      onComplete(accumulated);
      eventSource.close();
    });

    return () => eventSource.close();
  }

  async getFiles(projectId) {
    const response = await fetch(`${this.baseUrl}/api/projects/${projectId}/files`);
    return await response.json();
  }
}

// Usage
const client = new OutcomistClient('http://localhost:8000');

const project = await client.createProject(
  'My Game',
  'A platformer',
  'game'
);

await client.sendMessage(
  sessionId,
  'Create a simple game',
  (chunk, fullText) => console.log('Chunk:', chunk),
  (complete) => console.log('Complete:', complete)
);
```

## Next Steps

- Add authentication
- Implement rate limiting
- Add API versioning
- Create official client libraries
- Add WebSocket support
- Implement caching
- Add request validation
- Improve error messages

## Support

For API questions:
- Check this documentation
- Review [User Guide](USER_GUIDE.md)
- Report issues on GitHub
- Check backend logs for debugging
