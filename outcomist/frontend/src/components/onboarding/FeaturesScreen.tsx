interface FeaturesScreenProps {
  onNext: () => void;
  onBack: () => void;
}

const features = [
  {
    icon: '🎮',
    title: 'Games',
    description: 'Create interactive browser games with HTML, CSS, and JavaScript',
  },
  {
    icon: '✈️',
    title: 'Trip Planning',
    description: 'Plan detailed itineraries with AI-powered recommendations',
  },
  {
    icon: '✍️',
    title: 'Content',
    description: 'Generate articles, stories, and marketing copy',
  },
  {
    icon: '📊',
    title: 'Presentations',
    description: 'Build slide decks and presentation materials',
  },
];

export function FeaturesScreen({ onNext, onBack }: FeaturesScreenProps) {
  return (
    <div className="bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-12">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-[#e0e0e0] mb-3">What Can You Create?</h2>
        <p className="text-[#aaa]">Choose from multiple project types, each powered by AI</p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        {features.map(feature => (
          <div
            key={feature.title}
            className="bg-[rgba(30,30,30,0.5)] border border-white/5 rounded-lg p-6 text-center"
          >
            <div className="text-4xl mb-3">{feature.icon}</div>
            <h3 className="text-lg font-semibold text-[#e0e0e0] mb-2">{feature.title}</h3>
            <p className="text-sm text-[#888]">{feature.description}</p>
          </div>
        ))}
      </div>

      <div className="flex gap-4 justify-center">
        <button
          onClick={onBack}
          className="px-6 py-3 bg-transparent border border-white/20 text-[#aaa] hover:text-[#e0e0e0] hover:border-white/30 rounded-lg font-semibold transition-colors"
        >
          Back
        </button>
        <button
          onClick={onNext}
          className="px-6 py-3 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-semibold transition-colors"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
