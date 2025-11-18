import { Project, Session, Message, ProjectType } from '../types';

const API_BASE = '/api';

// Named export for convenience
export const api = {
  // Projects
  getProjects: async (): Promise<Project[]> => {
    const response = await fetch(`${API_BASE}/projects`);
    if (!response.ok) throw new Error('Failed to fetch projects');
    return response.json();
  },

  getProject: async (id: string): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects/${id}`);
    if (!response.ok) throw new Error('Failed to fetch project');
    return response.json();
  },

  createProject: async (data: {
    name: string;
    description?: string;
    type: ProjectType;
  }): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
  },

  updateProject: async (
    id: string,
    data: Partial<Pick<Project, 'name' | 'description' | 'status'>>
  ): Promise<Project> => {
    const response = await fetch(`${API_BASE}/projects/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update project');
    return response.json();
  },

  deleteProject: async (id: string): Promise<void> => {
    const response = await fetch(`${API_BASE}/projects/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete project');
  },

  // Sessions
  getSessions: async (projectId: string): Promise<Session[]> => {
    const response = await fetch(`${API_BASE}/projects/${projectId}/sessions`);
    if (!response.ok) throw new Error('Failed to fetch sessions');
    return response.json();
  },

  createSession: async (projectId: string, name: string): Promise<Session> => {
    const response = await fetch(`${API_BASE}/projects/${projectId}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    if (!response.ok) throw new Error('Failed to create session');
    return response.json();
  },

  // Messages
  getMessages: async (sessionId: string): Promise<Message[]> => {
    const response = await fetch(`${API_BASE}/sessions/${sessionId}/messages`);
    if (!response.ok) throw new Error('Failed to fetch messages');
    return response.json();
  },

  sendMessage: async (
    sessionId: string,
    content: string,
    stream = true
  ): Promise<Response> => {
    const response = await fetch(
      `${API_BASE}/sessions/${sessionId}/messages?stream=${stream}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      }
    );
    if (!response.ok) throw new Error('Failed to send message');
    return response;
  },
};

// Default export for compatibility
export default api;

// Alias for legacy imports
export const apiClient = api;
