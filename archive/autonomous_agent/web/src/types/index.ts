/**
 * TypeScript types matching the backend API
 */

// Task status values matching backend state machine
export type TaskStatus =
  | 'pending'
  | 'planning'
  | 'executing'
  | 'verifying'
  | 'completed'
  | 'failed';

// API request types
export interface CreateTaskRequest {
  goal: string;
  context?: string;
  constraints?: string[];
}

// Core task data structure
export interface Task {
  task_id: string;
  goal: string;
  context?: string;
  constraints?: string[];
  status: TaskStatus;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  current_activity?: string;
  elapsed_time?: number;
  progress?: string;
}

// Verification check result
export interface VerificationCheck {
  check: string;
  passed: boolean;
  details?: string;
}

// Task result structure
export interface TaskResult {
  task_id: string;
  success: boolean;
  artifacts: TaskArtifact[];
  validation: {
    overall_confidence: number;
    confidence: number;
    checks: VerificationCheck[];
    issues: string[];
  };
  error_message?: string;
}

// Individual artifact from task execution
export interface TaskArtifact {
  name: string;
  path: string;
  type: string;
  size?: number;
  content?: any;
}

// API response wrappers
export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}
