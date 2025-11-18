"""
Code Execution Tool: Execute Python code.

MVP Implementation:
- Direct execution using exec() (no sandbox)
- Captures stdout and return values
- Basic error handling

Future V1.0:
- Docker-based sandboxing
- Resource limits (CPU, memory, time)
- Security scanning
"""

import logging
import sys
from io import StringIO
from typing import Any, Dict

from ..core.working_memory import WorkingMemory

logger = logging.getLogger(__name__)


def execute(inputs: Dict[str, Any], memory: WorkingMemory) -> Dict[str, Any]:
    """
    Execute Python code.

    Args:
        inputs: Dictionary containing:
            - code: Python code string to execute
            - context: Optional dict of variables to make available
        memory: Working memory for artifact access

    Returns:
        Dictionary containing:
            - content: Execution result (stdout + return value)
            - content_type: "code_result"
            - stdout: Captured stdout
            - error: Error message if execution failed
            - success: Boolean indicating success
    """
    code = inputs.get("code", "")
    context = inputs.get("context", {})

    if not code:
        return {
            "content": "",
            "content_type": "code_result",
            "error": "No code provided",
            "success": False,
        }

    logger.info(f"Executing code: {code[:100]}...")

    # Capture stdout
    stdout_buffer = StringIO()
    original_stdout = sys.stdout

    try:
        sys.stdout = stdout_buffer

        # Create execution namespace
        exec_globals = {"__builtins__": __builtins__, "memory": memory}
        exec_globals.update(context)

        # Execute code
        exec(code, exec_globals)

        # Capture stdout
        stdout_content = stdout_buffer.getvalue()

        # Get result if code assigned to 'result' variable
        result_value = exec_globals.get("result", None)

        # Capture all variables created during execution (excluding builtins and memory)
        created_vars = {}
        for var_name, var_value in exec_globals.items():
            if not var_name.startswith("__") and var_name not in ["memory", "result"]:
                # Only capture simple types that can be serialized
                if isinstance(var_value, (str, int, float, bool, list, dict, type(None))):
                    created_vars[var_name] = var_value

        logger.info("Code execution completed successfully")
        if created_vars:
            logger.info(f"Captured variables: {list(created_vars.keys())}")

        return {
            "content": {
                "stdout": stdout_content,
                "result": result_value,
                "variables": created_vars,  # Include all created variables
            },
            "content_type": "code_result",
            "stdout": stdout_content,
            "success": True,
        }

    except Exception as e:
        error_msg = f"Code execution failed: {str(e)}"
        logger.error(error_msg)
        # Re-raise so executor can handle retry logic
        raise RuntimeError(error_msg) from e

    finally:
        sys.stdout = original_stdout
        stdout_buffer.close()
