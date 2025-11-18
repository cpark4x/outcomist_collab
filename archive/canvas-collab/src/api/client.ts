const API_BASE = 'http://localhost:3001/api';

export interface Workspace {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  widgets?: Widget[];
}

export interface Widget {
  id: string;
  workspace_id: string;
  type: string;
  position_x: number;
  position_y: number;
  width: number;
  height: number;
  data: any;
}

export const api = {
  // Workspace operations
  async createWorkspace(name: string): Promise<Workspace> {
    const response = await fetch(`${API_BASE}/workspaces`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    return response.json();
  },

  async listWorkspaces(): Promise<Workspace[]> {
    const response = await fetch(`${API_BASE}/workspaces`);
    return response.json();
  },

  async getWorkspace(id: string): Promise<Workspace> {
    const response = await fetch(`${API_BASE}/workspaces/${id}`);
    return response.json();
  },

  async updateWorkspace(id: string, name: string): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/workspaces/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    return response.json();
  },

  // Widget operations
  async createWidget(widget: Omit<Widget, 'id'>): Promise<Widget> {
    const response = await fetch(`${API_BASE}/widgets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        workspaceId: widget.workspace_id,
        type: widget.type,
        positionX: widget.position_x,
        positionY: widget.position_y,
        width: widget.width,
        height: widget.height,
        data: widget.data,
      }),
    });
    return response.json();
  },

  async updateWidget(id: string, updates: Partial<Widget>): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/widgets/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        positionX: updates.position_x,
        positionY: updates.position_y,
        width: updates.width,
        height: updates.height,
        data: updates.data,
      }),
    });
    return response.json();
  },

  async deleteWidget(id: string): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/widgets/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  // Claude AI operations
  async sendToAgent(widgetId: string, message: string, onChunk: (text: string) => void, onComplete: () => void, onError: (error: string) => void) {
    const response = await fetch(`${API_BASE}/agent/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ widgetId, message }),
    });

    if (!response.ok) {
      throw new Error('Failed to start agent');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) throw new Error('No reader available');

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));

            if (data.type === 'output') {
              onChunk(data.text);
            } else if (data.type === 'complete') {
              onComplete();
            } else if (data.type === 'error') {
              onError(data.message);
            }
          }
        }
      }
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Unknown error');
    }
  },

  async stopAgent(widgetId: string): Promise<{ success: boolean }> {
    const response = await fetch(`${API_BASE}/agent/stop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ widgetId }),
    });
    return response.json();
  },
};
