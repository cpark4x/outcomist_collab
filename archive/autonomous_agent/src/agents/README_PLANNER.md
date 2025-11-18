# Planner Agent Module

**Brick**: Self-contained planning module
**Stud**: `plan()` and `replan()` functions with clear TaskIntent → ExecutionPlan contract

## Purpose

Convert user intentions (TaskIntent) into detailed, executable plans (ExecutionPlan) with proper dependencies, tool assignments, and success criteria.

## Contract

### Inputs

**TaskIntent**:
```python
TaskIntent(
    goal: str,                    # What user wants to accomplish
    context: dict[str, Any],      # Additional information
    constraints: dict[str, Any],  # Limitations or requirements
    user_id: str,                 # User identifier
    task_id: Optional[str]        # Task identifier
)
```

### Outputs

**ExecutionPlan**:
```python
ExecutionPlan(
    task_id: str,
    steps: List[Step],                # 3-5 executable steps
    success_criteria: dict[str, Any], # Measurable outcomes
    estimated_duration: int           # Total seconds
)
```

Each `Step` contains:
- `step_id`: Unique identifier
- `tool`: ToolType (code_exec, filesystem, research, etc.)
- `inputs`: Tool-specific parameters
- `expected_output`: JSON schema for validation
- `timeout`: Maximum execution time in seconds
- `dependencies`: List of step_ids that must complete first

### Side Effects

- **LLM API calls**: Claude API via anthropic SDK
- **Logging**: Planning decisions logged for auditability
- **Retries**: Up to 3 attempts with exponential backoff

## Public Interface

```python
from src.agents.planner import PlannerAgent

# Initialize
planner = PlannerAgent(
    api_key="your_api_key",
    model="claude-3-5-sonnet-20241022",
    max_retries=3
)

# Generate initial plan
plan = planner.plan(intent)

# Regenerate plan after failure
new_plan = planner.replan(
    failed_step=step,
    error="error message",
    memory=working_memory,
    original_intent=intent
)
```

## Error Handling

| Error Type | Condition | Recovery Strategy |
|------------|-----------|-------------------|
| ValueError | Invalid dependencies | Raise with details |
| RuntimeError | API unavailable after retries | Raise with retry count |
| KeyError | Unknown tool type | Default to CODE_EXEC with warning |
| JSONDecodeError | Invalid API response | Retry with backoff |

## Performance Characteristics

- **API call latency**: ~2-5 seconds per plan
- **Retry delays**: 1s, 2s, 4s (exponential backoff)
- **Plan complexity**: 3-5 steps for MVP
- **Timeout**: 300s default per step

## Configuration

```python
# Environment variables (optional)
ANTHROPIC_API_KEY=your_key_here

# Default model
MODEL = "claude-3-5-sonnet-20241022"

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1.0  # seconds
```

## Planning Strategy

The Planner uses Claude to:

1. **Analyze user intent** - Extract goals, context, constraints
2. **Identify required tools** - Map sub-tasks to appropriate tools
3. **Define dependencies** - Establish execution order
4. **Specify success criteria** - Define measurable outcomes
5. **Estimate duration** - Provide realistic time expectations

### Example Planning Flow

**Input**:
```python
TaskIntent(
    goal="Create a Python file that calculates fibonacci(10)",
    context={"language": "python"},
    constraints={"max_steps": 5}
)
```

**Generated Plan**:
```python
ExecutionPlan(
    task_id="task_123",
    steps=[
        Step(
            step_id="step_1",
            tool=ToolType.RESEARCH,
            inputs={"query": "fibonacci algorithm"},
            dependencies=[],
            timeout=300
        ),
        Step(
            step_id="step_2",
            tool=ToolType.CODE_EXEC,
            inputs={"code": "def fibonacci(n): ..."},
            dependencies=["step_1"],
            timeout=300
        ),
        Step(
            step_id="step_3",
            tool=ToolType.FILESYSTEM,
            inputs={"path": "fibonacci.py", "content": "..."},
            dependencies=["step_2"],
            timeout=300
        )
    ],
    success_criteria={
        "primary": ["File exists", "Code runs", "Output is 55"],
        "validation": ["Syntax valid", "Function defined"]
    },
    estimated_duration=900
)
```

## Testing

```bash
# Run planner tests
pytest tests/test_planner.py -v

# Test with coverage
pytest tests/test_planner.py --cov=src/agents/planner
```

### Test Coverage

- ✅ Plan generation from intent
- ✅ Dependency validation
- ✅ Retry logic with exponential backoff
- ✅ Error handling and recovery
- ✅ Replanning after failures
- ✅ Ready steps identification

## Dependencies

- `anthropic>=0.39.0` - Claude API client
- `src.core.contracts` - Data type contracts
- `src.core.working_memory` - Context retrieval

## Regeneration Specification

This module can be fully regenerated from this specification. Key invariants:

1. **Function signatures**:
   - `plan(intent: TaskIntent) -> ExecutionPlan`
   - `replan(failed_step, error, memory, original_intent) -> ExecutionPlan`

2. **Input/output structures**: TaskIntent and ExecutionPlan from contracts.py

3. **Error types**:
   - ValueError for validation errors
   - RuntimeError for API failures

4. **Side effects**:
   - Claude API calls
   - Logging via Python logging module

## Design Decisions

### Why 3-5 steps?

**Simplicity**: MVP focuses on manageable plans. Future versions can support larger plans with sub-planning.

### Why exponential backoff?

**API reliability**: Transient errors are common. Exponential backoff prevents hammering the API while giving it time to recover.

### Why validate dependencies?

**Safety**: Invalid dependencies cause execution failures. Better to catch early during planning.

### Why logging?

**Auditability**: Planning decisions affect execution. Logs enable debugging and analysis.

## Future Enhancements

- Sub-planning for complex tasks (V1.0)
- Parallel execution support (V1.0)
- Cost estimation (V1.0)
- Plan optimization (V2.0)
- Learning from past plans (V2.0)
