import { Session } from '../../types';

interface SessionTabsProps {
  sessions: Session[];
  currentSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onDeleteSession?: (sessionId: string) => void;
}

export function SessionTabs({ sessions, currentSessionId, onSelectSession, onDeleteSession }: SessionTabsProps) {
  // Only show tabs if there are multiple sessions
  if (sessions.length <= 1) return null;

  return (
    <div className="flex gap-1 px-3 py-2 bg-[rgba(37,37,37,0.4)] border-b border-white/[0.03] overflow-x-auto">
      {sessions.map((session) => (
        <div
          key={session.id}
          className={`px-3 py-1.5 rounded-md cursor-pointer relative flex items-center gap-2 transition-all duration-150 min-w-[140px] group ${
            session.id === currentSessionId
              ? 'bg-[rgba(74,144,226,0.15)] border border-[rgba(74,144,226,0.3)]'
              : 'bg-transparent border border-transparent hover:bg-white/[0.03]'
          }`}
          onClick={() => onSelectSession(session.id)}
        >
          <div className="flex flex-col gap-0.5 text-left flex-1">
            <div
              className={`text-[10px] font-semibold uppercase tracking-wide ${
                session.id === currentSessionId ? 'text-[#4A90E2]' : 'text-[#666]'
              }`}
            >
              Session {sessions.indexOf(session) + 1}
            </div>
            <div
              className={`text-[11px] font-medium truncate ${
                session.id === currentSessionId ? 'text-[#e0e0e0]' : 'text-[#aaa]'
              }`}
            >
              {session.name}
            </div>
          </div>
          {onDeleteSession && sessions.length > 1 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDeleteSession(session.id);
              }}
              className="opacity-0 group-hover:opacity-100 w-4 h-4 flex items-center justify-center text-[#888] hover:text-[#ff6b6b] transition-all"
              title="Delete session"
            >
              ×
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
