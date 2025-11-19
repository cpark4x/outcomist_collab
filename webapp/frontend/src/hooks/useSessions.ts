import { useState, useEffect } from 'react';
import { Session } from '../types';
import { api } from '../api/client';

export function useSessions(projectId: string | null) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchSessions = async () => {
    if (!projectId) {
      setSessions([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const data = await api.getSessions(projectId);
      setSessions(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, [projectId]);

  return { sessions, loading, error, refetch: fetchSessions };
}
