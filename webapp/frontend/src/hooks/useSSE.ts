import { useEffect, useState, useCallback } from 'react';
import { SSEEvent } from '../types';

export function useSSE(sessionId: string | null) {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [connected, setConnected] = useState(false);

  const connect = useCallback(() => {
    if (!sessionId) return;

    const es = new EventSource(`/api/sessions/${sessionId}/stream`);

    es.onopen = () => {
      setConnected(true);
      console.log('SSE connected');
    };

    es.onmessage = (event) => {
      try {
        const data: SSEEvent = JSON.parse(event.data);
        setEvents((prev) => [...prev, data]);
      } catch (err) {
        console.error('Failed to parse SSE event:', err);
      }
    };

    es.onerror = () => {
      setConnected(false);
      console.error('SSE error');
    };

    return () => {
      es.close();
      setConnected(false);
    };
  }, [sessionId]);

  useEffect(() => {
    const cleanup = connect();
    return cleanup;
  }, [connect]);

  const clearEvents = () => setEvents([]);

  return { events, connected, clearEvents };
}
