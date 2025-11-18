interface WelcomeScreenProps {
  onNext: () => void;
  onSkip?: () => void;
}

export function WelcomeScreen({ onNext, onSkip }: WelcomeScreenProps) {
  return (
    <div className="bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-12 text-center">
      <div className="text-6xl mb-6">🚀</div>
      <h1 className="text-4xl font-bold text-[#e0e0e0] mb-4">Welcome to Outcomist</h1>
      <p className="text-lg text-[#aaa] mb-8 max-w-md mx-auto">
        Your AI-powered workspace for creating games, planning trips, generating content, and building
        presentations.
      </p>
      <div className="flex gap-4 justify-center">
        <button
          onClick={onNext}
          className="px-6 py-3 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-semibold transition-colors"
        >
          Get Started
        </button>
        {onSkip && (
          <button
            onClick={onSkip}
            className="px-6 py-3 bg-transparent border border-white/20 text-[#aaa] hover:text-[#e0e0e0] hover:border-white/30 rounded-lg font-semibold transition-colors"
          >
            Skip Tour
          </button>
        )}
      </div>
    </div>
  );
}
