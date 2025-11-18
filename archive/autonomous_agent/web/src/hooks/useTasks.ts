/**
 * Tanstack Query hooks for task management
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import type { CreateTaskRequest, TaskStatus } from '../types';

// Query keys for cache management
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (filters: { status?: TaskStatus }) => [...taskKeys.lists(), filters] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
  results: () => [...taskKeys.all, 'result'] as const,
  result: (id: string) => [...taskKeys.results(), id] as const,
};

// Hook to get all tasks
export function useTasks() {
  return useQuery({
    queryKey: taskKeys.lists(),
    queryFn: () => api.getTasks(),
    staleTime: 30000, // Consider fresh for 30s
  });
}

// Hook to get single task with auto-refresh for active tasks
export function useTask(taskId: string) {
  return useQuery({
    queryKey: taskKeys.detail(taskId),
    queryFn: () => api.getTask(taskId),
    enabled: !!taskId,
    refetchInterval: (query) => {
      // Poll every 2s if task is active
      const activeStatuses: TaskStatus[] = ['pending', 'planning', 'executing', 'verifying'];
      return query.state.data && activeStatuses.includes(query.state.data.status) ? 2000 : false;
    },
  });
}

// Hook to get task result
export function useTaskResult(taskId: string, enabled: boolean = true) {
  return useQuery({
    queryKey: taskKeys.result(taskId),
    queryFn: () => api.getTaskResult(taskId),
    enabled: enabled && !!taskId,
  });
}

// Hook to create new task
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTaskRequest) => api.createTask(data),
    onSuccess: () => {
      // Invalidate task list to show new task
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}

// Hook to download artifact
export function useDownloadArtifact() {
  return useMutation({
    mutationFn: ({ taskId, artifactPath }: { taskId: string; artifactPath: string }) =>
      api.downloadArtifact(taskId, artifactPath),
    onSuccess: (blobUrl, { artifactPath }) => {
      // Trigger download
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = artifactPath.split('/').pop() || 'artifact';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
    },
  });
}
