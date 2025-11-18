import type { Widget, Workspace } from './widget';

export interface IPCChannels {
  // Workspace operations
  'workspace:create': (name: string) => Promise<Workspace>;
  'workspace:load': (id: string) => Promise<Workspace>;
  'workspace:save': (workspace: Workspace) => Promise<void>;
  'workspace:list': () => Promise<Workspace[]>;

  // Widget operations
  'widget:create': (workspaceId: string, widget: Omit<Widget, 'id'>) => Promise<Widget>;
  'widget:update': (widget: Widget) => Promise<void>;
  'widget:delete': (widgetId: string) => Promise<void>;

  // Agent operations
  'agent:send': (widgetId: string, message: string) => Promise<void>;
  'agent:stop': (widgetId: string) => Promise<void>;

  // Tool operations
  'tool:execute': (widgetId: string, toolName: string, input: any) => Promise<any>;
}

export interface IPCEvents {
  'agent:output': (widgetId: string, chunk: string) => void;
  'agent:tool-use': (widgetId: string, toolUse: any) => void;
  'agent:error': (widgetId: string, error: string) => void;
  'agent:complete': (widgetId: string) => void;
}
