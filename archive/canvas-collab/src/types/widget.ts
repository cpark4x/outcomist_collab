export type WidgetType = 'agent' | 'document' | 'filebrowser' | 'generated-app';

export interface Position {
  x: number;
  y: number;
}

export interface Size {
  width: number;
  height: number;
}

export interface Widget {
  id: string;
  type: WidgetType;
  position: Position;
  size: Size;
  zIndex: number;
  title: string;
  state?: Record<string, any>;
}

export interface AgentWidgetState {
  conversationId: string;
  messages: Message[];
  isStreaming: boolean;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  toolUse?: ToolUse[];
}

export interface ToolUse {
  id: string;
  name: string;
  input: Record<string, any>;
  output?: string;
  error?: string;
}

export interface Workspace {
  id: string;
  name: string;
  pan: Position;
  zoom: number;
  widgets: Widget[];
  createdAt: number;
  updatedAt: number;
}
