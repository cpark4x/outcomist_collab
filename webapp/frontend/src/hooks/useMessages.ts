import { useState, useEffect } from 'react';
import { Message } from '../types';
import { api } from '../api/client';

export function useMessages(sessionId: string | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchMessages = async () => {
    if (!sessionId) {
      setMessages([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const data = await api.getMessages(sessionId);
      setMessages(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [sessionId]);

  const addMessage = (message: Message) => {
    setMessages((prev) => [...prev, message]);
  };

  const updateMessage = (id: string, updates: Partial<Message>) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, ...updates } : msg))
    );
  };

  return { messages, loading, error, refetch: fetchMessages, addMessage, updateMessage };
}
