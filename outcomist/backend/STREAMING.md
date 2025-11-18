# Streaming with Server-Sent Events (SSE)

Outcomist supports real-time streaming of AI responses using Server-Sent Events (SSE). This enables a more interactive experience where users see the AI's response as it's being generated, rather than waiting for the complete response.

## Overview

SSE is a standard for pushing real-time updates from server to client over HTTP. Unlike WebSockets, SSE:
- Uses regular HTTP (simpler infrastructure)
- Automatically reconnects on disconnect
- Works through most proxies and firewalls
- Is unidirectional (server → client only)

## How It Works

1. **Client connects** to SSE endpoint with a message
2. **Server starts streaming** events as Claude generates the response
3. **Client receives** events in real-time and updates UI
4. **Connection closes** when response is complete

## Event Types

The streaming API emits the following event types:

### `message_start`
Emitted when streaming begins.

```json
{
  "type": "message_start",
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### `message_delta`
Emitted for each chunk of content as it arrives from Claude.

```json
{
  "type": "message_delta",
  "content": "Hello, "
}
```

### `message_complete`
Emitted when the complete response has been generated and saved.

```json
{
  "type": "message_complete",
  "message_id": "456e7890-e89b-12d3-a456-426614174000",
  "content": "Hello, how can I help you today?"
}
```

### `error`
Emitted if an error occurs during streaming.

```json
{
  "type": "error",
  "error": "Session not found"
}
```

## Endpoints

### Dedicated Streaming Endpoint

**GET** `/api/sessions/{session_id}/stream?message=<message>`

Dedicated SSE endpoint for streaming AI responses.

**Parameters:**
- `session_id` (path): UUID of the session
- `message` (query): User message to send to Claude

**Response:** SSE stream with `text/event-stream` content type

**Example:**
```bash
curl -N "http://localhost:8000/api/sessions/{session_id}/stream?message=What%20is%20decision%20science?"
```

### Message API with Streaming

**POST** `/api/sessions/{session_id}/messages?stream=true`

The standard message API can also return an SSE stream when `stream=true`.

**Parameters:**
- `session_id` (path): UUID of the session
- `stream` (query): Set to `true` for SSE streaming

**Body:**
```json
{
  "content": "What is decision science?"
}
```

**Response:**
- If `stream=true`: SSE stream
- If `stream=false` (default): JSON response with complete message pair

## Client Implementation

### JavaScript (Browser)

```javascript
const sessionId = 'your-session-id';
const message = 'What is decision science?';

// Build URL with query parameters
const params = new URLSearchParams({ message });
const url = `http://localhost:8000/api/sessions/${sessionId}/stream?${params}`;

// Create EventSource
const eventSource = new EventSource(url);

// Handle connection open
eventSource.onopen = () => {
  console.log('Connected to SSE stream');
};

// Handle incoming messages
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case 'message_start':
      console.log('Streaming started');
      break;

    case 'message_delta':
      // Append content as it arrives
      document.getElementById('response').textContent += data.content;
      break;

    case 'message_complete':
      console.log('Streaming complete:', data.message_id);
      eventSource.close();
      break;

    case 'error':
      console.error('Error:', data.error);
      eventSource.close();
      break;
  }
};

// Handle errors
eventSource.onerror = (error) => {
  console.error('EventSource error:', error);
  eventSource.close();
};
```

### Python

```python
import json
import requests

session_id = 'your-session-id'
message = 'What is decision science?'

url = f"http://localhost:8000/api/sessions/{session_id}/stream"
params = {'message': message}

response = requests.get(url, params=params, stream=True, timeout=60)
response.raise_for_status()

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')

        # Skip comments (heartbeats)
        if line_str.startswith(':'):
            continue

        # Parse data events
        if line_str.startswith('data: '):
            data_str = line_str[6:]  # Remove "data: " prefix
            data = json.loads(data_str)

            if data['type'] == 'message_delta':
                print(data['content'], end='', flush=True)
            elif data['type'] == 'message_complete':
                print(f"\n\nComplete! Message ID: {data['message_id']}")
                break
            elif data['type'] == 'error':
                print(f"\n\nError: {data['error']}")
                break
```

### cURL

```bash
curl -N "http://localhost:8000/api/sessions/{session_id}/stream?message=What%20is%20decision%20science?"
```

The `-N` flag disables buffering so events appear immediately.

## Connection Management

### Active Connections

The server tracks active SSE connections using a `ConnectionManager`. This allows:
- Multiple clients to watch the same session
- Broadcasting status updates to all connected clients
- Clean disconnect handling

### Heartbeats

The server sends periodic heartbeat comments (`: heartbeat\n\n`) every 15 seconds to keep the connection alive. Clients should ignore these.

### Reconnection

If the connection drops, browsers automatically attempt to reconnect. You can configure this behavior:

```javascript
// Disable automatic reconnection
eventSource.close();

// Or handle reconnection yourself
eventSource.onerror = (error) => {
  eventSource.close();
  // Wait and reconnect
  setTimeout(() => {
    eventSource = new EventSource(url);
  }, 5000);
};
```

## Error Handling

### Common Errors

**Session not found:**
```json
{
  "type": "error",
  "error": "Session 123e4567-e89b-12d3-a456-426614174000 not found"
}
```

**API errors:**
```json
{
  "type": "error",
  "error": "Anthropic API error: Rate limit exceeded"
}
```

### Best Practices

1. **Always handle errors**: Listen for `error` events and close the connection
2. **Set timeouts**: Use reasonable timeouts (30-60 seconds) to avoid hanging connections
3. **Close when done**: Always close the EventSource when finished
4. **Handle disconnects**: Implement reconnection logic with exponential backoff

## Testing

### Test Script

Use the provided test script:

```bash
python test_streaming.py <session_id> "Your message here"
```

### HTML Test Client

Open `examples/sse_client.html` in a browser for an interactive test client.

### Manual Testing

1. Start the server: `uvicorn src.main:app --reload`
2. Create a project and session using the API
3. Connect to the streaming endpoint with the session ID
4. Send a message and watch the response stream in real-time

## Performance Considerations

### Buffering

- SSE responses are unbuffered (immediate delivery)
- The `X-Accel-Buffering: no` header disables nginx buffering
- Use `-N` flag with curl to disable client-side buffering

### Concurrency

- Each SSE connection holds an async coroutine
- Server can handle hundreds of concurrent streams
- Use connection pooling for multiple simultaneous clients

### Memory Usage

- Message content is accumulated in memory during streaming
- Complete message is saved to database only after streaming finishes
- Memory usage scales with message length, not stream duration

## Architecture

### Flow Diagram

```
Client                 API Server              Claude API
  |                        |                        |
  |-- GET /stream -------->|                        |
  |                        |-- Stream request ----->|
  |<-- message_start ------|                        |
  |                        |<-- Text chunk ---------|
  |<-- message_delta ------|                        |
  |                        |<-- Text chunk ---------|
  |<-- message_delta ------|                        |
  |                        |<-- Stream complete ----|
  |                        |-- Save to DB --------->|
  |<-- message_complete ---|                        |
  |                        |                        |
```

### Components

- **`src/ai/events.py`**: SSE event types and formatting
- **`src/ai/streaming.py`**: Streaming AI service using Claude async API
- **`src/api/streaming.py`**: SSE endpoint handlers
- **`src/services/connection_manager.py`**: Active connection tracking
- **`src/api/messages.py`**: Updated message API with streaming support

## Migration from Synchronous

If you have existing code using the synchronous message API:

```javascript
// Old (synchronous)
const response = await fetch('/api/sessions/{id}/messages', {
  method: 'POST',
  body: JSON.stringify({ content: message })
});
const data = await response.json();
console.log(data.ai_message.content);

// New (streaming)
const url = `/api/sessions/{id}/stream?message=${encodeURIComponent(message)}`;
const eventSource = new EventSource(url);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'message_delta') {
    console.log(data.content);
  }
};
```

Both approaches are supported. Use streaming for better UX, synchronous for simpler implementation.

## Security Considerations

### CORS

The server is configured with CORS to allow browser-based SSE clients. Adjust `settings.cors_origins` in production.

### Rate Limiting

Consider adding rate limiting to prevent abuse:
- Limit connections per session
- Limit concurrent streams per user
- Implement backpressure for slow clients

### Authentication

Add authentication middleware to verify clients before establishing SSE connections.

## Troubleshooting

### Events not appearing

**Problem:** No events received after connecting

**Solutions:**
- Check that server is running and accessible
- Verify session ID is valid
- Check browser console for connection errors
- Disable any buffering proxies (nginx, etc.)

### Duplicate events

**Problem:** Same content appears multiple times

**Solutions:**
- Ensure you're not creating multiple EventSource instances
- Close previous connections before opening new ones
- Check for browser extension interference

### Connection drops

**Problem:** Connection closes unexpectedly

**Solutions:**
- Increase timeout values
- Check server logs for errors
- Implement reconnection logic
- Verify network stability

### Slow streaming

**Problem:** Large delays between events

**Solutions:**
- Check Claude API response times
- Verify no buffering is enabled
- Monitor server resource usage
- Use dedicated SSE endpoint (lower overhead)

## Next Steps

With streaming implemented, you can:
- Build a real-time chat interface
- Show typing indicators
- Implement progress bars
- Add pause/resume functionality
- Stream to multiple viewers simultaneously

For frontend integration, see the Phase 3 documentation.
