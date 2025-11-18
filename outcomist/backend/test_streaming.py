"""Test script for SSE streaming functionality.

Usage:
    python test_streaming.py <session_id> <message>

Example:
    python test_streaming.py 123e4567-e89b-12d3-a456-426614174000 "What is decision science?"
"""

import json
import sys
from urllib.parse import urlencode

import requests


def test_sse_stream(session_id: str, message: str, base_url: str = "http://localhost:8000"):
    """Test SSE streaming endpoint.

    Args:
        session_id: Session ID to stream
        message: User message to send
        base_url: Base URL of API server
    """
    # Build URL with query parameters
    params = urlencode({"message": message})
    url = f"{base_url}/api/sessions/{session_id}/stream?{params}"

    print(f"Connecting to: {url}")
    print(f"Message: {message}")
    print("-" * 80)

    try:
        # Connect with streaming
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        # Process SSE events
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")

                # Skip comments (heartbeats)
                if line_str.startswith(":"):
                    continue

                # Parse data events
                if line_str.startswith("data: "):
                    data_str = line_str[6:]  # Remove "data: " prefix
                    try:
                        data = json.loads(data_str)
                        event_type = data.get("type")

                        if event_type == "message_start":
                            print("\n🚀 Streaming started...")

                        elif event_type == "message_delta":
                            # Print content as it arrives
                            content = data.get("content", "")
                            print(content, end="", flush=True)

                        elif event_type == "message_complete":
                            message_id = data.get("message_id")
                            print(f"\n\n✅ Complete! Message ID: {message_id}")

                        elif event_type == "error":
                            error = data.get("error")
                            print(f"\n\n❌ Error: {error}")
                            break

                    except json.JSONDecodeError as e:
                        print(f"\nWarning: Could not parse JSON: {e}")
                        print(f"Raw line: {line_str}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        sys.exit(1)

    print("\n" + "-" * 80)


def test_message_api_streaming(session_id: str, message: str, base_url: str = "http://localhost:8000"):
    """Test message API with stream=true parameter.

    Args:
        session_id: Session ID
        message: User message to send
        base_url: Base URL of API server
    """
    url = f"{base_url}/api/sessions/{session_id}/messages?stream=true"

    print("Testing message API with streaming")
    print(f"URL: {url}")
    print(f"Message: {message}")
    print("-" * 80)

    try:
        response = requests.post(
            url,
            json={"content": message},
            stream=True,
            timeout=60,
        )
        response.raise_for_status()

        # Process SSE events
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")

                if line_str.startswith(":"):
                    continue

                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    try:
                        data = json.loads(data_str)
                        event_type = data.get("type")

                        if event_type == "message_start":
                            print("\n🚀 Streaming started...")

                        elif event_type == "message_delta":
                            content = data.get("content", "")
                            print(content, end="", flush=True)

                        elif event_type == "message_complete":
                            message_id = data.get("message_id")
                            print(f"\n\n✅ Complete! Message ID: {message_id}")

                        elif event_type == "error":
                            error = data.get("error")
                            print(f"\n\n❌ Error: {error}")
                            break

                    except json.JSONDecodeError as e:
                        print(f"\nWarning: Could not parse JSON: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        sys.exit(1)

    print("\n" + "-" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    session_id = sys.argv[1]
    message = sys.argv[2]

    print("\n=== Test 1: Dedicated streaming endpoint ===\n")
    test_sse_stream(session_id, message)

    print("\n=== Test 2: Message API with stream=true ===\n")
    test_message_api_streaming(session_id, message)
