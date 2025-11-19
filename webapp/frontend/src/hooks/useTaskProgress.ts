import { useState, useEffect } from 'react';
import { Task, TaskState } from '../components/project/TaskProgressCard';

// Map WorkPhase to user-friendly task labels
const PHASE_TO_TASK: Record<string, string> = {
  understanding: 'Understand your request',
  planning: 'Plan the game structure',
  thinking: 'Design game mechanics',
  generating: 'Create game files',
  tool_use: 'Build game components',
  complete: 'Finalize and verify',
};

// Task order for consistent display
const TASK_ORDER = [
  'understanding',
  'planning',
  'thinking',
  'generating',
  'tool_use',
  'complete',
];

export function useTaskProgress(projectId: string) {
  const [tasks, setTasks] = useState<Task[]>(() => {
    // Try to load from localStorage
    const stored = localStorage.getItem(`task_progress_${projectId}`);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        // Fall through to initial state
      }
    }

    // Initialize with all tasks as pending
    return TASK_ORDER.map(phase => ({
      id: phase,
      label: PHASE_TO_TASK[phase],
      state: 'pending' as TaskState,
    }));
  });

  // Update task state based on phase
  const updateTaskFromPhase = (phase: string, statusMessage?: string) => {
    setTasks(prevTasks => {
      const phaseIndex = TASK_ORDER.indexOf(phase);
      if (phaseIndex === -1) return prevTasks;

      const newTasks = prevTasks.map((task, index) => {
        const taskPhase = TASK_ORDER[index];

        if (index < phaseIndex) {
          // Previous tasks are completed
          return {
            ...task,
            state: 'completed' as TaskState,
            completedAt: task.completedAt || Date.now(),
            statusMessage: undefined, // Clear status on completion
          };
        } else if (index === phaseIndex) {
          // Current task is active
          return {
            ...task,
            state: 'active' as TaskState,
            startedAt: task.startedAt || Date.now(),
            statusMessage: statusMessage || task.statusMessage, // Update with current activity
          };
        } else {
          // Future tasks are pending
          return task;
        }
      });

      // Persist to localStorage
      localStorage.setItem(`task_progress_${projectId}`, JSON.stringify(newTasks));

      return newTasks;
    });
  };

  // Mark all tasks as complete
  const completeAllTasks = () => {
    setTasks(prevTasks => {
      const completedTasks = prevTasks.map(task => ({
        ...task,
        state: 'completed' as TaskState,
        completedAt: task.completedAt || Date.now(),
      }));

      localStorage.setItem(`task_progress_${projectId}`, JSON.stringify(completedTasks));
      return completedTasks;
    });
  };

  // Reset tasks
  const resetTasks = () => {
    const initialTasks = TASK_ORDER.map(phase => ({
      id: phase,
      label: PHASE_TO_TASK[phase],
      state: 'pending' as TaskState,
    }));

    setTasks(initialTasks);
    localStorage.removeItem(`task_progress_${projectId}`);
  };

  return {
    tasks,
    updateTaskFromPhase,
    completeAllTasks,
    resetTasks,
  };
}
