"""Claude AI tools definitions."""

FILE_TOOL = {
    "name": "create_file",
    "description": "Create or update a file in the project. Use this to generate code, HTML, CSS, JavaScript, or any other file content.",
    "input_schema": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Name of the file (e.g., 'game.html', 'style.css', 'script.js')",
            },
            "content": {
                "type": "string",
                "description": "The complete file content",
            },
            "mime_type": {
                "type": "string",
                "description": "MIME type (e.g., 'text/html', 'text/javascript', 'text/css'). Defaults to 'text/plain'",
            },
        },
        "required": ["filename", "content"],
    },
}

UPDATE_PROJECT_NAME_TOOL = {
    "name": "update_project_name",
    "description": "Update the project name to reflect what is being built. Call this on the first message to give the project a descriptive name based on the user's request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Short, descriptive project name (e.g., 'Tic Tac Toe Game', 'Vegas Trip Planner')",
            },
        },
        "required": ["name"],
    },
}

TOOLS = [FILE_TOOL, UPDATE_PROJECT_NAME_TOOL]
