import { useState, useEffect } from 'react';
import type { File } from '../types';

const API_BASE = '/api';

export function useFiles(projectId: string | null) {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId) {
      setFiles([]);
      return;
    }

    const fetchFiles = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_BASE}/projects/${projectId}/files`);
        if (!response.ok) throw new Error('Failed to fetch files');
        const data = await response.json();
        setFiles(data);
      } catch (err) {
        console.error('Error fetching files:', err);
        setError('Failed to load files');
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [projectId]);

  const refreshFiles = async () => {
    if (!projectId) return;

    try {
      const response = await fetch(`${API_BASE}/projects/${projectId}/files`);
      if (!response.ok) throw new Error('Failed to fetch files');
      const data = await response.json();
      setFiles(data);
    } catch (err) {
      console.error('Error refreshing files:', err);
    }
  };

  return { files, loading, error, refreshFiles };
}

export function useFileContent(fileId: string | null) {
  const [content, setContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!fileId) {
      setContent(null);
      return;
    }

    const fetchContent = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_BASE}/files/${fileId}/content`);
        if (!response.ok) throw new Error('Failed to fetch content');
        const data = await response.json();
        setContent(data.content);
      } catch (err) {
        console.error('Error fetching file content:', err);
        setError('Failed to load file content');
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, [fileId]);

  return { content, loading, error };
}
