import { useRef, useEffect } from 'react';
import { Message, ProjectStatus } from '../../types';

interface ActivityBarProps {
  status: ProjectStatus;
  messages: Message[];
  collapsed: boolean;
  onToggle: () => void;
  onViewAgent: () => void;
  compact?: boolean;
}

const statusMessages: Record<ProjectStatus, string> = {
  idle: 'Waiting for task',
  planning: 'Analyzing your request...',
  working: 'Creating deliverables...',
  needs_input: 'Waiting for your response',
  verifying: 'Checking quality...',
  complete: 'Task complete',
};

export function ActivityBar({ status, messages, collapsed, onToggle, onViewAgent, compact = false }: ActivityBarProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Don't show bar when idle AND no messages yet
  if (status === 'idle' && messages.length === 0) {
    return null;
  }

  // Get latest AI message
  const latestAIMessage = messages
    .filter((m) => m.role === 'assistant')
    .slice(-1)[0];

  // Check if currently streaming
  const isStreaming = latestAIMessage?.status === 'streaming';

  const statusMessage = statusMessages[status];
  // Show full content while streaming, truncated when complete
  const activitySummary = isStreaming
    ? latestAIMessage?.content || statusMessage
    : latestAIMessage?.content?.substring(0, 150) || statusMessage;

  // Auto-scroll to bottom when streaming
  useEffect(() => {
    if (isStreaming && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [activitySummary, isStreaming]);

  return (
    <div
      className={`border-b border-slate-500/20 transition-all duration-200 ${
        collapsed ? 'h-12' : compact ? 'h-auto max-h-24' : 'h-auto max-h-48'
      }`}
      style={{
        backgroundColor: 'rgba(30, 41, 59, 0.6)',
      }}
    >
      {/* Collapsed View */}
      {collapsed && (
        <div
          className="h-full px-4 flex items-center gap-3 cursor-pointer hover:bg-slate-700/30 transition-colors"
          onClick={onToggle}
        >
          <div className="flex items-center gap-2 flex-1">
            {/* Status indicator */}
            <div
              className={`w-2 h-2 rounded-full ${
                isStreaming
                  ? 'animate-pulse-typing'
                  : status === 'planning' || status === 'working' || status === 'verifying'
                  ? 'animate-pulse-status'
                  : ''
              }`}
              style={{
                backgroundColor:
                  status === 'planning'
                    ? '#93C5FD'
                    : status === 'working'
                    ? '#86EFAC'
                    : status === 'verifying'
                    ? '#D8B4FE'
                    : status === 'complete'
                    ? '#86EFAC'
                    : '#9CA3AF',
              }}
            />
            <span className="text-sm text-slate-300 font-medium">{statusMessage}</span>
          </div>
          <svg
            className="w-4 h-4 text-slate-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      )}

      {/* Expanded View */}
      {!collapsed && (
        <div className="p-4">
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  status === 'planning' || status === 'working' || status === 'verifying'
                    ? 'animate-pulse-status'
                    : ''
                }`}
                style={{
                  backgroundColor:
                    status === 'planning'
                      ? '#93C5FD'
                      : status === 'working'
                      ? '#86EFAC'
                      : status === 'verifying'
                      ? '#D8B4FE'
                      : status === 'complete'
                      ? '#86EFAC'
                      : '#9CA3AF',
                }}
              />
              <span className="text-sm font-semibold text-slate-200">{statusMessage}</span>
            </div>
            <button
              onClick={onToggle}
              className="text-slate-400 hover:text-slate-200 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
              </svg>
            </button>
          </div>

          {/* Activity Summary */}
          <div ref={scrollRef} className="text-xs text-slate-400 mb-3 max-h-24 overflow-y-auto leading-relaxed">
            {activitySummary}
            {!isStreaming && activitySummary.length >= 150 && '...'}
            {isStreaming && <span className="inline-block w-1 h-3 bg-slate-400 animate-pulse ml-1">|</span>}
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <button
              onClick={onViewAgent}
              className="px-3 py-1.5 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/40 rounded-md text-xs text-blue-300 transition-colors"
            >
              View Full Conversation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
