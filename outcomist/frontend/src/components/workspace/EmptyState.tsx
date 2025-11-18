interface EmptyStateProps {
  onCreateProject: () => void;
}

export function EmptyState({ onCreateProject }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-57px)] px-10">
      <div className="text-center max-w-[600px]">
        <div className="text-5xl font-bold bg-gradient-to-r from-[#667eea] to-[#764ba2] bg-clip-text text-transparent mb-6">
          Welcome to Outcomist
        </div>
        <p className="text-lg text-[#aaa] mb-10 leading-relaxed">
          Your AI-powered multi-project workspace. Create your first project to get started.
        </p>
        <button
          onClick={onCreateProject}
          className="bg-gradient-to-br from-[#667eea] to-[#764ba2] text-white border-none px-8 py-4 rounded-xl cursor-pointer text-base font-semibold transition-all duration-300 shadow-[0_4px_20px_rgba(102,126,234,0.3)] hover:translate-y-[-2px] hover:shadow-[0_6px_30px_rgba(102,126,234,0.4)]"
        >
          + Create Your First Project
        </button>
      </div>
    </div>
  );
}
