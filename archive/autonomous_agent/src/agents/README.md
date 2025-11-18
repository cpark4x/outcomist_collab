# Executor Agent

The Executor Agent is responsible for executing steps from an execution plan and generating artifacts.

## Purpose

Execute tools and generate artifacts according to an execution plan, with proper error handling, retry logic, and full auditability.

## Contract

### Inputs
- `ExecutionPlan`: Complete plan with ordered steps
- `WorkingMemory`: Persistent storage for artifacts and state

### Outputs
- `List[Artifact]`: All artifacts generated during execution

### Side Effects
- Tool execution (code, filesystem, research)
- Memory writes (artifacts, step status, plan status)
- Status updates in working memory

## Public Interface

```python
from src.agents.executor import ExecutorAgent
from src.core.working_memory import WorkingMemory
from src.core.contracts import ExecutionPlan

# Initialize
memory = WorkingMemory(task_id="my_task")
executor = ExecutorAgent(memory, max_retries=3)

# Execute complete plan
artifacts = executor.execute_plan(plan)

# Execute single step
artifact = executor.execute_step(step)

# Execute ready steps (dependency-aware)
artifacts = executor.execute_ready_steps(plan)
```

## Implementation Details

### Sequential Execution

Steps are executed one at a time in order. Each step:
1. Status updated to RUNNING
2. Tool dispatched based on step.tool
3. Result captured and wrapped in Artifact
4. Artifact stored in Working Memory
5. Status updated to COMPLETED or FAILED

### Error Handling

- **Retry Logic**: Up to `max_retries` attempts per step (default: 3)
- **Exponential Backoff**: 2^attempt seconds between retries
- **Graceful Degradation**: Failed steps don't crash the entire plan
- **Detailed Logging**: All errors logged with context

### Tool Registry

Available tools:
- `CODE_EXEC`: Execute Python code
- `FILESYSTEM`: Read/write files
- `RESEARCH`: Query and synthesize information

### Timeout Enforcement

Each step has a `timeout` (default: 300s). If execution exceeds this:
- TimeoutError raised
- Retry logic triggered
- Status set to FAILED after retries exhausted

### Provenance Tracking

Every artifact maintains a provenance chain:
- Created by which step
- Depends on which artifacts
- Full lineage traceable

## Tool Implementations

### Code Execution Tool

**Location**: `src/tools/code_exec.py`

**MVP**: Direct execution using `exec()` (no sandbox)

**Future V1.0**: Docker-based sandboxing, resource limits

**Example**:
```python
inputs = {
    "code": "result = 2 + 2",
    "context": {"x": 10}  # Optional variables
}
result = code_exec.execute(inputs, memory)
# result["content"]["result"] == 4
```

### Filesystem Tool

**Location**: `src/tools/filesystem.py`

**Operations**: read, write

**Example**:
```python
# Read file
inputs = {
    "operation": "read",
    "path": "/path/to/file.txt"
}

# Write file
inputs = {
    "operation": "write",
    "path": "/path/to/output.txt",
    "content": "Hello, World!"
}
```

### Research Tool

**Location**: `src/tools/research.py`

**MVP**: Mock research data

**Future V1.0**: LLM-powered research with web search

**Example**:
```python
inputs = {
    "query": "Python best practices",
    "sources": ["web", "documentation"],
    "depth": "medium"  # shallow, medium, deep
}
```

## Testing

Run the test suite:
```bash
cd autonomous_agent
uv run pytest tests/test_executor.py -v
```

**Test Coverage**:
- ✅ Single step execution (all tool types)
- ✅ Complete plan execution
- ✅ Retry logic on failure
- ✅ Provenance tracking
- ✅ Status tracking
- ✅ Artifact storage

## Performance Characteristics

- **Time complexity**: O(n) for n steps (sequential)
- **Memory usage**: O(k) for k artifacts stored
- **Retry overhead**: Exponential backoff (2^attempt seconds)

## Configuration

```python
executor = ExecutorAgent(
    memory=memory,
    max_retries=3  # Number of retry attempts per step
)
```

## Error Types

| Error | Condition | Recovery |
|-------|-----------|----------|
| `ExecutionError` | Step fails after all retries | Plan fails, error logged |
| `TimeoutError` | Step exceeds timeout | Retry triggered |
| `RuntimeError` | Tool execution fails | Retry triggered |

## Regeneration Specification

This module can be regenerated from this specification alone.

**Key invariants**:
- `execute_step()` signature and return type
- `execute_plan()` signature and return type
- Tool registry structure
- Artifact creation logic
- Retry behavior (exponential backoff, max 3 attempts)

**Changeable**:
- Tool implementations (as long as they follow the contract)
- Logging details
- Internal helper methods

## Design Principles

- **Ruthless Simplicity**: Sequential execution, no premature optimization
- **Fail Gracefully**: Retry logic prevents transient failures
- **Full Auditability**: Every action logged and stored
- **Clear Contracts**: Well-defined inputs/outputs for all functions
- **Testability**: All logic unit-testable

## Future Enhancements (V1.0)

- [ ] Parallel execution of independent steps
- [ ] Docker-based sandboxing for code execution
- [ ] Resource limits (CPU, memory, disk)
- [ ] Security scanning for code
- [ ] LLM-powered research tool
- [ ] Web search integration
- [ ] More sophisticated retry strategies
