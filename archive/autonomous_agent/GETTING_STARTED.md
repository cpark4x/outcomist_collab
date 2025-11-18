# Getting Started with Autonomous Agent

**Quick start guide for running your first autonomous task**

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com))
- 5 minutes

## Step 1: Installation

```bash
# Navigate to the project directory
cd autonomous_agent

# Install dependencies
pip install -e .

# Verify installation
python -c "from src.api import app; print('✓ Installation successful!')"
```

## Step 2: Set API Key

```bash
# Export your Anthropic API key
export ANTHROPIC_API_KEY='sk-ant-api03-...'

# Verify it's set
echo $ANTHROPIC_API_KEY
```

## Step 3: Start the Server

```bash
# Option 1: Use the startup script
./run_server.sh

# Option 2: Start directly
uvicorn src.api:app --reload --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Step 4: Submit Your First Task

Open a new terminal and run:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Create a Python file that calculates fibonacci(10) and prints the result",
    "context": {},
    "constraints": {}
  }'
```

You'll get a response like:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Task submitted successfully. Use GET /tasks/{task_id} to check status."
}
```

## Step 5: Check Status

```bash
# Replace with your actual task_id
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "executing",
  "progress": "Executing plan steps and generating artifacts",
  "started_at": "2025-01-17T10:30:01.234Z",
  "updated_at": "2025-01-17T10:30:05.678Z"
}
```

Possible statuses:
- `pending` - Task queued
- `planning` - Generating execution plan
- `executing` - Running tools
- `verifying` - Validating outputs
- `completed` - Task finished successfully
- `failed` - Task encountered an error

## Step 6: Get Results

Once status is `completed`, retrieve the results:

```bash
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000/result
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "success": true,
  "artifacts": [
    {
      "artifact_id": "...",
      "content": "fibonacci.py file created",
      "content_type": "file_path",
      "metadata": {
        "path": "workspace/fibonacci.py"
      }
    }
  ],
  "validation": {
    "passed": true,
    "confidence": 0.95,
    "checks": [...]
  },
  "execution_time": 8.5,
  "completed_at": "2025-01-17T10:30:10.123Z"
}
```

## Step 7: Verify the Output

Check that the file was created:

```bash
# View the generated file
cat workspace/fibonacci.py

# Run it
python workspace/fibonacci.py
```

## Example Tasks to Try

### 1. Simple File Creation

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Create a file hello.txt with the content: Hello, Autonomous Agent!"
  }'
```

### 2. Data Processing

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Calculate the sum of numbers from 1 to 100 and save the result to sum.txt"
  }'
```

### 3. Code Generation

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Create a Python function that checks if a string is a palindrome, with examples",
    "context": {
      "include_tests": true
    }
  }'
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive API documentation where you can:
- Submit tasks through a web interface
- See all available endpoints
- View request/response schemas
- Test the API without curl

## Troubleshooting

### API Key Not Found

```bash
# Error: "ANTHROPIC_API_KEY environment variable not set"
# Solution: Export your API key
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

### Server Won't Start

```bash
# Error: "Address already in use"
# Solution: Kill process on port 8000 or use different port
lsof -ti:8000 | xargs kill -9
# Or use different port
uvicorn src.api:app --port 8001
```

### Import Errors

```bash
# Error: "ModuleNotFoundError: No module named 'src'"
# Solution: Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Task Stuck in "pending"

```bash
# Check server logs for errors
# Likely causes:
# 1. API key invalid
# 2. Network issues
# 3. Server crashed

# Restart server and try again
./run_server.sh
```

### Database Locked

```bash
# Error: "database is locked"
# Solution: Clear memory directory
rm -rf memory/*.db

# Or wait a few seconds and retry
```

## Understanding the Workflow

### What Happens When You Submit a Task

1. **Planning** (2-5s)
   - Planner Agent converts your goal into 3-5 step execution plan
   - Plan stored in Working Memory

2. **Execution** (varies)
   - Executor Agent runs each step sequentially
   - Tools execute (code, filesystem, research)
   - Artifacts stored in Working Memory

3. **Verification** (1-3s)
   - Verifier Agent validates outputs independently
   - Checks: schema compliance, logical consistency, structural integrity
   - Issues flagged if validation fails

4. **Result** (instant)
   - Consolidated TaskResult returned
   - Includes: artifacts, validation, plan, execution time

### Total Time

- Simple tasks: 5-15 seconds
- Complex tasks: 30-60 seconds
- Target: <45s for simple, <7min for complex

## Next Steps

1. **Read the Full Documentation**
   - [README.md](./README.md) - Complete user guide
   - [docs/README_API.md](./docs/README_API.md) - API reference
   - [SECURITY.md](./SECURITY.md) - Security considerations

2. **Explore the Architecture**
   - [src/agents/README_PLANNER.md](./src/agents/README_PLANNER.md)
   - [src/agents/README_EXECUTOR.md](./src/agents/README_EXECUTOR.md)
   - [src/agents/README_VERIFIER.md](./src/agents/README_VERIFIER.md)

3. **Run the Tests**
   ```bash
   pytest tests/ -v
   ```

4. **Try More Complex Tasks**
   - Multi-file projects
   - Data analysis workflows
   - Code refactoring

5. **Review Execution Logs**
   ```bash
   # Check working memory databases
   ls -lh memory/

   # View server logs
   tail -f logs/server.log  # if logging configured
   ```

## Getting Help

- **Documentation**: All READMEs in this repository
- **Issues**: Create a GitHub issue
- **Security**: See [SECURITY.md](./SECURITY.md)
- **API Docs**: http://localhost:8000/docs

## What's Next

This is an **MVP (Phase 0)** implementation. Coming soon:

- **Week 3**: Docker sandbox for secure code execution
- **Week 4**: Enhanced error recovery and performance optimization
- **V1.0**: Authentication, parallelization, browser automation, UI layer

See [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) for the complete roadmap.

---

**Ready to build?** Submit your first task and watch the autonomous agent work! 🚀
