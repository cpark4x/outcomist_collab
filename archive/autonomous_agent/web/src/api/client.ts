/**
 * API client with typed fetch wrappers for backend communication
 */

import type { Task, TaskResult, CreateTaskRequest, TaskListResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Generic API error class
export class ApiError extends Error {
  public status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

// Generic fetch wrapper with error handling
async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(response.status, errorText || response.statusText);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(0, `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// API response for task creation
interface CreateTaskResponse {
  task_id: string;
  status: string;
  message: string;
  submitted_at: string;
}

// API client methods
export const api = {
  // Create new task
  createTask: (data: CreateTaskRequest): Promise<CreateTaskResponse> => {
    return fetchApi<CreateTaskResponse>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Get task by ID
  getTask: (taskId: string): Promise<Task> => {
    return fetchApi<Task>(`/tasks/${taskId}`);
  },

  // Get all tasks
  getTasks: (): Promise<TaskListResponse> => {
    return fetchApi<TaskListResponse>('/tasks');
  },

  // Get task result
  getTaskResult: (taskId: string): Promise<TaskResult> => {
    return fetchApi<TaskResult>(`/tasks/${taskId}/result`);
  },

  // Download artifact (returns blob URL)
  downloadArtifact: async (taskId: string, artifactPath: string): Promise<string> => {
    const url = `${API_BASE_URL}/tasks/${taskId}/artifacts/${encodeURIComponent(artifactPath)}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new ApiError(response.status, 'Failed to download artifact');
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  },
};
