export type ProjectType = 'game' | 'trip' | 'content' | 'presentation';
export type ProjectStatus = 'idle' | 'planning' | 'working' | 'needs_input' | 'verifying' | 'complete';
export type MessageRole = 'user' | 'assistant' | 'system';
export type MessageStatus = 'pending' | 'streaming' | 'complete' | 'error';
export type ProgressPhase = 'understanding' | 'planning' | 'thinking' | 'generating' | 'tool_use' | 'complete';

export interface ProgressData {
  phase: ProgressPhase;
  percentage: number;
  statusText: string;
  step?: {
    current: number;
    total: number;
  };
  startTime: Date;
  filename?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  type: ProjectType;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
  current_session_id: string | null;
}

export interface Session {
  id: string;
  project_id: string;
  name: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  status: MessageStatus;
  progress?: ProgressData;
}

export interface File {
  id: string;
  project_id: string;
  session_id: string | null;
  name: string;
  mime_type: string;
  size: number;
  created_at: string;
}

export interface SSEEvent {
  type: 'message_start' | 'message_delta' | 'message_complete' | 'status_update' | 'error';
  session_id?: string;
  project_id?: string;
  content?: string;
  message?: Message;
  status?: ProjectStatus;
  status_message?: string;
  status_context?: {
    agent?: 'planner' | 'executor' | 'verifier';
    step?: string;
  };
  previous_status?: ProjectStatus;
  error?: string;
}
