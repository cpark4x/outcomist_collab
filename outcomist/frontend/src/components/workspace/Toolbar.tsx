type ViewMode = 'grid' | 'list';

interface ToolbarProps {
  onNewProject: () => void;
  stats?: {
    projects: number;
    sessions: number;
    messages: number;
  };
  viewMode: ViewMode;
  onViewModeChange: (mode: ViewMode) => void;
}

export function Toolbar({ onNewProject, stats, viewMode, onViewModeChange }: ToolbarProps) {
  return (
    <div className="bg-[rgba(42,42,42,0.95)] backdrop-blur-[20px] border-b border-white/5 px-6 py-3.5 flex items-center gap-5 relative z-[100] shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
      <div className="flex items-center gap-5">
        <div className="text-sm font-semibold text-[#e0e0e0]">
          <span className="text-2xl font-bold bg-gradient-to-r from-[#667eea] to-[#764ba2] bg-clip-text text-transparent">
            Outcomist
          </span>
        </div>
      </div>
      <div className="ml-auto flex items-center gap-3">
        {/* Lightweight Stats */}
        {stats && (
          <div className="flex items-center gap-4 text-xs text-[#888] mr-2">
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-[#aaa]">{stats.projects}</span>
              <span>projects</span>
            </div>
            <div className="w-1 h-1 bg-[#666] rounded-full"></div>
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-[#aaa]">{stats.sessions}</span>
              <span>sessions</span>
            </div>
            <div className="w-1 h-1 bg-[#666] rounded-full"></div>
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-[#aaa]">{stats.messages}</span>
              <span>messages</span>
            </div>
          </div>
        )}

        {/* View Mode Toggle */}
        <div className="flex gap-1 bg-[#1e1e1e] p-1 rounded-lg">
          <button
            onClick={() => onViewModeChange('grid')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              viewMode === 'grid'
                ? 'bg-blue-500/20 text-blue-400'
                : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
            }`}
          >
            Grid
          </button>
          <button
            onClick={() => onViewModeChange('list')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              viewMode === 'list'
                ? 'bg-blue-500/20 text-blue-400'
                : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
            }`}
          >
            List
          </button>
        </div>

        <button
          onClick={onNewProject}
          className="bg-gradient-to-br from-[#4A90E2] to-[#357ABD] text-white border-none px-4 py-2 rounded-lg cursor-pointer text-sm font-semibold transition-all duration-200 shadow-[0_2px_8px_rgba(74,144,226,0.3)] hover:translate-y-[-1px] hover:shadow-[0_4px_12px_rgba(74,144,226,0.4)]"
        >
          + New Project
        </button>
      </div>
    </div>
  );
}
