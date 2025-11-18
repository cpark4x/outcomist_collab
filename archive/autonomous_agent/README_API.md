# Autonomous Agent API

REST API for autonomous task execution using the P→E→V (Planner → Executor → Verifier) workflow.

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
cd autonomous_agent
uv sync

# Or using pip
pip install -e .
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### 3. Start the Server

```bash
# Option 1: Using the startup script
./run_server.sh

# Option 2: Directly with Python
python -m src.api

# Option 3: With uvicorn (for development)
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /
```

Check if the API is running.

**Response:**
```json
{
  "service": "Autonomous Agent API",
  "version": "0.1.0",
  "status": "running"
}
```

---

### Submit Task
```bash
POST /tasks
```

Submit a new task for autonomous execution.

**Request Body:**
```json
{
  "goal": "Create a Python file that prints 'Hello, World!'",
  "context": {
    "language": "python",
    "filename": "hello.py"
  },
  "constraints": {
    "max_lines": 10
  },
  "user_id": "user_123"
}
```

**Response (202 Accepted):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Task submitted successfully. Use task_id to query status.",
  "submitted_at": "2025-01-17T10:30:00.000Z"
}
```

---

### Get Task Status
```bash
GET /tasks/{task_id}
```

Query the current status of a task.

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "executing",
  "progress": "Executing plan steps and generating artifacts",
  "started_at": "2025-01-17T10:30:01.000Z",
  "completed_at": null,
  "error": null
}
```

**Possible statuses:**
- `pending` - Task queued for execution
- `planning` - Analyzing task and generating execution plan
- `executing` - Executing plan steps
- `verifying` - Verifying artifacts against success criteria
- `completed` - Task completed successfully
- `failed` - Task execution failed

---

### Get Task Result
```bash
GET /tasks/{task_id}/result
```

Retrieve the final result of a completed task.

**Response (200 OK):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "success": true,
  "artifacts": [
    {
      "artifact_id": "abc123",
      "content": "print('Hello, World!')",
      "content_type": "code",
      "created_by": "step_1",
      "metadata": {
        "language": "python",
        "filename": "hello.py"
      }
    }
  ],
  "validation": {
    "passed": true,
    "confidence": 0.95,
    "checks": [
      {
        "check_type": "schema",
        "passed": true,
        "details": "Artifact matches expected schema"
      }
    ],
    "issues": []
  },
  "execution_time": 12.5,
  "plan": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "steps": [...]
  },
  "completed_at": "2025-01-17T10:30:13.500Z",
  "error": null
}
```

**Error Responses:**
- `404 Not Found` - Task ID not found
- `409 Conflict` - Task not yet completed (still in progress)

---

## Example Usage

### Using cURL

```bash
# 1. Submit a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Create a Python file that prints Hello, World!",
    "context": {"language": "python"}
  }'

# Response: {"task_id": "abc-123", ...}

# 2. Check status
curl http://localhost:8000/tasks/abc-123

# 3. Get result (when completed)
curl http://localhost:8000/tasks/abc-123/result
```

### Using Python

```python
import requests
import time

# 1. Submit task
response = requests.post(
    "http://localhost:8000/tasks",
    json={
        "goal": "Create a Python file that prints 'Hello, World!'",
        "context": {"language": "python"}
    }
)
task_id = response.json()["task_id"]
print(f"Task submitted: {task_id}")

# 2. Poll for completion
while True:
    status_response = requests.get(f"http://localhost:8000/tasks/{task_id}")
    status = status_response.json()["status"]
    print(f"Status: {status}")

    if status in ["completed", "failed"]:
        break

    time.sleep(2)

# 3. Get result
result_response = requests.get(f"http://localhost:8000/tasks/{task_id}/result")
result = result_response.json()
print(f"Success: {result['success']}")
print(f"Artifacts: {len(result['artifacts'])}")
```

## Running Tests

### Integration Tests

The integration test suite validates the complete P→E→V workflow through the API.

```bash
# 1. Start the server (in one terminal)
./run_server.sh

# 2. Run tests (in another terminal)
python tests/test_api_integration.py
```

### What the Tests Validate

1. **API Health** - Server is running and responding
2. **Task Submission** - Task is accepted and queued
3. **Status Polling** - Can track task progress
4. **Result Retrieval** - Can get final results
5. **Result Validation** - Results have correct structure:
   - Artifacts are present and valid
   - Validation result is complete
   - Execution plan is included
   - Success status matches expectations

## Architecture

```
User Request → FastAPI Server → Orchestrator → P→E→V Flow
                    ↓
              Background Task
                    ↓
        ┌───────────────────────┐
        │  Working Memory (DB)  │
        └───────────────────────┘
                    ↓
        ┌───────────────────────┐
        │   Planner Agent       │ Generate ExecutionPlan
        └───────────────────────┘
                    ↓
        ┌───────────────────────┐
        │   Executor Agent      │ Execute Steps → Artifacts
        └───────────────────────┘
                    ↓
        ┌───────────────────────┐
        │   Verifier Agent      │ Validate → ValidationResult
        └───────────────────────┘
                    ↓
               TaskResult
```

## Configuration

Environment variables:

- `ANTHROPIC_API_KEY` - **Required** - API key for Claude
- `MEMORY_DIR` - Optional - Directory for working memory storage (default: `./memory`)

## Error Handling

The API provides comprehensive error handling:

1. **Planning Failures** - Automatic retry with exponential backoff
2. **Execution Failures** - Attempt replan with alternative approach
3. **Verification Failures** - Return result with detailed issues
4. **Timeout Handling** - Graceful cancellation of long-running tasks

All errors are logged and returned with helpful messages.

## Development

### Project Structure

```
autonomous_agent/
├── src/
│   ├── core/
│   │   ├── orchestrator.py    # P→E→V coordination
│   │   ├── contracts.py        # Data types
│   │   └── working_memory.py   # Persistent storage
│   ├── agents/
│   │   ├── planner.py         # Planning agent
│   │   ├── executor.py        # Execution agent
│   │   └── verifier.py        # Verification agent
│   ├── tools/
│   │   ├── code_exec.py       # Code execution tool
│   │   ├── filesystem.py      # File operations
│   │   └── research.py        # Research tool
│   └── api.py                 # FastAPI server
├── tests/
│   └── test_api_integration.py
├── memory/                     # Working memory storage
├── pyproject.toml
└── README_API.md
```

### Adding New Features

1. **New Tool** - Add to `src/tools/` and register in `ExecutorAgent`
2. **New Validation** - Add check type in `VerifierAgent`
3. **New Endpoint** - Add route in `src/api.py`

## Troubleshooting

### Server won't start
- Check that port 8000 is not already in use
- Verify Python 3.11+ is installed
- Ensure dependencies are installed (`uv sync`)

### Tasks fail with API errors
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check API key has sufficient credits
- Review server logs for detailed error messages

### Tasks timeout
- Increase `MAX_WAIT_TIME` in test script for complex tasks
- Check network connectivity to Anthropic API
- Review execution logs in working memory

## API Documentation

When the server is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

See project root for license information.
