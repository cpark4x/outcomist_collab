interface ToolbarProps {
  onNewProject: () => void;
}

export function Toolbar({ onNewProject }: ToolbarProps) {
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
