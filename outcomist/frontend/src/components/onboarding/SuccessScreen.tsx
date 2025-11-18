interface SuccessScreenProps {
  onFinish: () => void;
}

export function SuccessScreen({ onFinish }: SuccessScreenProps) {
  return (
    <div className="bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-12 text-center">
      <div className="text-6xl mb-6">🎉</div>
      <h2 className="text-3xl font-bold text-[#e0e0e0] mb-4">You're All Set!</h2>
      <p className="text-lg text-[#aaa] mb-8 max-w-md mx-auto">
        Your project has been created. Let's start building something amazing together!
      </p>
      <button
        onClick={onFinish}
        className="px-8 py-4 bg-[#4A90E2] hover:bg-[#357ABD] text-white text-lg rounded-lg font-semibold transition-colors"
      >
        Go to Workspace
      </button>
    </div>
  );
}
