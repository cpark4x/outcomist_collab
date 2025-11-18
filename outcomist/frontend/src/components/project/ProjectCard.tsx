import { useState, useEffect, useRef } from 'react';
import { Project } from '../../types';
import { StatusBadge } from './StatusBadge';
import { SessionTabs } from './SessionTabs';
import { AgentView } from './AgentView';
import { PreviewView } from './PreviewView';
import { FilesView } from './FilesView';
import { InlineInput } from './InlineInput';
import { ActivityBar } from './ActivityBar';
import { useSessions } from '../../hooks/useSessions';
import { useMessages } from '../../hooks/useMessages';
import { api } from '../../api/client';

interface ProjectCardProps {
  project: Project;
  onDelete?: (projectId: string) => void;
  className?: string;
  viewMode?: 'grid' | 'list';
}

type ViewType = 'agent' | 'preview' | 'files';

const projectIcons: Record<string, string> = {
  game: '🎮',
  trip: '✈️',
  content: '✍️',
  presentation: '📊',
};

export function ProjectCard({ project, onDelete, className, viewMode = 'grid' }: ProjectCardProps) {
  const [currentView, setCurrentView] = useState<ViewType>('agent');
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    project.current_session_id
  );
  const [activityBarCollapsed, setActivityBarCollapsed] = useState(true);
  const [prevStatus, setPrevStatus] = useState(project.status);

  // Track if we're creating a session to prevent race conditions
  const creatingSessionRef = useRef(false);

  const { sessions, loading: sessionsLoading } = useSessions(project.id);
  const { messages, addMessage, updateMessage, refetch: refetchMessages } = useMessages(currentSessionId);

  // Auto-create session if none exists - wait for loading to complete
  useEffect(() => {
    const initSession = async () => {
      // Wait for sessions to finish loading before making decisions
      if (sessionsLoading) return;

      // Prevent creating multiple sessions simultaneously
      if (creatingSessionRef.current) return;

      if (sessions.length === 0 && !currentSessionId) {
        // No sessions exist and none being created - create one
        creatingSessionRef.current = true;
        try {
          const session = await api.createSession(project.id, 'Main Session');
          setCurrentSessionId(session.id);
        } catch (error) {
          console.error('Failed to create session:', error);
        } finally {
          creatingSessionRef.current = false;
        }
      } else if (sessions.length > 0 && !currentSessionId) {
        // Sessions exist but none selected - use the first one
        setCurrentSessionId(sessions[0].id);
      }
    };
    initSession();
  }, [sessions, sessionsLoading, currentSessionId, project.id]);

  // Auto-expand activity bar on status change or streaming
  useEffect(() => {
    const hasStreamingMessage = messages.some(
      (m) => m.role === 'assistant' && m.status === 'streaming'
    );

    if (project.status !== prevStatus) {
      setPrevStatus(project.status);

      // Expand when status changes to active state
      if (project.status !== 'idle' && project.status !== 'complete') {
        setActivityBarCollapsed(false);
      }

      // Auto-collapse 10s after completion
      if (project.status === 'complete') {
        const timer = setTimeout(() => {
          setActivityBarCollapsed(true);
        }, 10000);
        return () => clearTimeout(timer);
      }
    } else if (hasStreamingMessage && activityBarCollapsed) {
      // Expand when streaming starts
      setActivityBarCollapsed(false);
    }
  }, [project.status, prevStatus, messages, activityBarCollapsed]);

  const handleSendMessage = async (content: string) => {
    if (!currentSessionId) return;

    // Add user message immediately
    const userMessage = {
      id: `temp-user-${Date.now()}`,
      session_id: currentSessionId,
      role: 'user' as const,
      content,
      timestamp: new Date().toISOString(),
      status: 'complete' as const,
    };
    addMessage(userMessage);

    // Create placeholder for assistant response with progress tracking
    const assistantMessageId = `temp-assistant-${Date.now()}`;
    const startTime = new Date();
    addMessage({
      id: assistantMessageId,
      session_id: currentSessionId,
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      status: 'streaming',
      progress: {
        phase: 'understanding',
        percentage: 0,
        statusText: 'Starting...',
        startTime,
      },
    });

    try {
      const response = await api.sendMessage(currentSessionId, content, true);

      // Handle SSE streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let accumulatedContent = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            // Handle both "data: " and "data: data: " prefixes
            let data = '';
            if (line.startsWith('data: data: ')) {
              data = line.slice(12).trim();
            } else if (line.startsWith('data: ')) {
              data = line.slice(6).trim();
            } else {
              continue;
            }

            if (!data) continue;

            try {
              const parsed = JSON.parse(data);

              // Handle different event types
              if (parsed.type === 'status_update') {
                // Update progress data
                updateMessage(assistantMessageId, {
                  progress: {
                    phase: parsed.phase,
                    percentage: parsed.progress * 100,
                    statusText: parsed.message,
                    startTime,
                  },
                });
              } else if (parsed.type === 'message_delta' && parsed.content) {
                accumulatedContent += parsed.content;
                updateMessage(assistantMessageId, {
                  content: accumulatedContent,
                  status: 'streaming',
                });
              } else if (parsed.type === 'message_complete') {
                updateMessage(assistantMessageId, {
                  status: 'complete',
                  progress: undefined, // Clear progress on completion
                });
              } else if (parsed.type === 'error') {
                updateMessage(assistantMessageId, {
                  content: `Error: ${parsed.error}`,
                  status: 'error',
                  progress: undefined,
                });
              }
            } catch (e) {
              console.error('Failed to parse SSE event:', e, 'Line:', line);
            }
          }
        }

        // Mark as complete if not already done
        updateMessage(assistantMessageId, {
          status: 'complete',
        });
      }

      // Don't refetch - backend already saved messages, and refetch erases our local state
      // await refetchMessages();
    } catch (error) {
      console.error('Failed to send message:', error);
      updateMessage(assistantMessageId, {
        content: 'Error: Failed to get response',
        status: 'error',
      });
    }
  };

  const cycleView = () => {
    const views: ViewType[] = ['agent', 'preview', 'files'];
    const currentIndex = views.indexOf(currentView);
    const nextIndex = (currentIndex + 1) % views.length;
    setCurrentView(views[nextIndex]);
  };

  const handleDelete = async () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${project.name}"?\n\nThis will:\n• Remove the project from your workspace\n• Delete all files\n• Preserve conversation history for learning`
    );

    if (!confirmed) return;

    try {
      await api.deleteProject(project.id);
      onDelete?.(project.id);
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert('Failed to delete project. Please try again.');
    }
  };

  const getViewButtonText = () => {
    switch (currentView) {
      case 'agent':
        return 'Preview';
      case 'preview':
        return 'Chat';
      case 'files':
        return 'Chat';
    }
  };

  const getViewButtonIcon = () => {
    switch (currentView) {
      case 'agent':
        return '👁️';
      case 'preview':
        return '💬';
      case 'files':
        return '💬';
    }
  };

  return (
    <div className={`bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-xl overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)] hover:border-[rgba(74,144,226,0.3)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.3)] flex flex-col ${className || 'h-[580px]'}`}>
      {/* Card Header */}
      <div
        className="px-4 py-2.5 flex items-center gap-3 bg-gradient-to-r from-slate-700/80 to-slate-600/80 border-b border-slate-500/30"
        style={{
          minHeight: '48px'
        }}
      >
        <div className="text-base">{projectIcons[project.type] || '📁'}</div>
        <div className="flex-1 text-[13px] font-semibold text-[#e0e0e0]">
          {project.name || 'Untitled Project'}
        </div>
        <StatusBadge status={project.status} />
        <button
          onClick={() => setCurrentView(currentView === 'agent' ? 'preview' : 'agent')}
          className="p-1 bg-transparent border border-white/10 rounded-md text-[#888] cursor-pointer transition-all duration-200 flex items-center justify-center w-6 h-6 hover:bg-white/5 hover:text-[#e0e0e0] hover:border-white/20"
          title={currentView === 'agent' ? 'Preview' : 'Chat'}
        >
          {currentView === 'agent' ? (
            <svg width="12" height="12" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 9a2 2 0 100-4 2 2 0 000 4z" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M1 7s2-4 6-4 6 4 6 4-2 4-6 4-6-4-6-4z" stroke="currentColor" strokeWidth="1.5"/>
            </svg>
          ) : (
            <svg width="12" height="12" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 7.5c0 2.5-2.2 4.5-5 4.5-.6 0-1.2-.1-1.7-.3L2 13l.8-3.3C2.3 9.2 2 8.4 2 7.5 2 5 4.2 3 7 3s5 2 5 4.5z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </button>
        <button
          onClick={() => setCurrentView('files')}
          className="p-1 bg-transparent border border-white/10 rounded-md text-[#888] cursor-pointer text-base transition-all duration-200 flex items-center justify-center w-6 h-6 hover:bg-white/5 hover:text-[#e0e0e0] hover:border-white/20"
          title="Files"
        >
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12H2V2h5l2 2h3v8z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        <button
          onClick={() => window.open(`/project/${project.id}`, '_blank')}
          className="p-1 bg-transparent border border-white/10 rounded-md text-[#888] cursor-pointer text-sm transition-all duration-200 flex items-center justify-center w-6 h-6 hover:bg-white/5 hover:text-[#e0e0e0] hover:border-white/20"
          title="Open in new window"
        >
          ⤢
        </button>
        <button
          onClick={handleDelete}
          className="p-1 bg-transparent border border-white/10 rounded-md text-[#888] cursor-pointer transition-all duration-200 flex items-center justify-center w-6 h-6 hover:bg-red-500/20 hover:text-red-400 hover:border-red-500/30"
          title="Delete project"
        >
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 4h10M5 4V3a1 1 0 011-1h2a1 1 0 011 1v1m1 0v7a1 1 0 01-1 1H5a1 1 0 01-1-1V4h6z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      {/* Session Tabs */}
      {currentView === 'agent' && (
        <SessionTabs
          sessions={sessions}
          currentSessionId={currentSessionId}
          onSelectSession={setCurrentSessionId}
        />
      )}

      {/* Activity Bar - Shows AI activity in all views */}
      <ActivityBar
        status={project.status}
        messages={messages}
        collapsed={activityBarCollapsed}
        onToggle={() => setActivityBarCollapsed(!activityBarCollapsed)}
        onViewAgent={() => setCurrentView('agent')}
        compact={viewMode === 'list'}
      />

      {/* Content Area */}
      <div className="relative bg-[rgba(30,30,30,0.3)] flex-1 flex flex-col overflow-hidden">
        {currentView === 'agent' && <AgentView messages={messages} />}
        {currentView === 'preview' && <PreviewView project={project} />}
        {currentView === 'files' && <FilesView projectId={project.id} />}
      </div>

      {/* Inline Input */}
      <InlineInput
        onSend={handleSendMessage}
        disabled={project.status === 'running'}
        placeholder="Type your response..."
      />
    </div>
  );
}
