#!/bin/bash
# Start the Autonomous Agent API server

echo "Starting Autonomous Agent API Server..."
echo "======================================"

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY environment variable not set"
    echo "   The API will not be able to execute tasks without it."
    echo ""
    echo "   Set it with: export ANTHROPIC_API_KEY='your-api-key'"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create memory directory if it doesn't exist
mkdir -p memory

echo ""
echo "Starting server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

# Run the server
cd "$(dirname "$0")"
python -m src.api
