import type { ProjectType } from '../../types';

interface ProjectTypeScreenProps {
  onSelectType: (type: ProjectType) => void;
  onBack: () => void;
  onSkip?: () => void;
}

const projectTypes: Array<{
  type: ProjectType;
  icon: string;
  title: string;
  description: string;
}> = [
  {
    type: 'game',
    icon: '🎮',
    title: 'Game',
    description: 'Create an interactive browser game',
  },
  {
    type: 'trip',
    icon: '✈️',
    title: 'Trip',
    description: 'Plan a detailed travel itinerary',
  },
  {
    type: 'content',
    icon: '✍️',
    title: 'Content',
    description: 'Generate written content',
  },
  {
    type: 'presentation',
    icon: '📊',
    title: 'Presentation',
    description: 'Build a slide deck',
  },
];

export function ProjectTypeScreen({ onSelectType, onBack, onSkip }: ProjectTypeScreenProps) {
  return (
    <div className="bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-12">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-[#e0e0e0] mb-3">Choose Your First Project</h2>
        <p className="text-[#aaa]">Select a project type to get started</p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        {projectTypes.map(pt => (
          <button
            key={pt.type}
            onClick={() => onSelectType(pt.type)}
            className="bg-[rgba(30,30,30,0.5)] border border-white/5 hover:border-[#4A90E2]/50 rounded-lg p-8 text-center transition-all hover:scale-105 hover:shadow-lg"
          >
            <div className="text-5xl mb-3">{pt.icon}</div>
            <h3 className="text-xl font-semibold text-[#e0e0e0] mb-2">{pt.title}</h3>
            <p className="text-sm text-[#888]">{pt.description}</p>
          </button>
        ))}
      </div>

      <div className="flex gap-4 justify-center">
        <button
          onClick={onBack}
          className="px-6 py-3 bg-transparent border border-white/20 text-[#aaa] hover:text-[#e0e0e0] hover:border-white/30 rounded-lg font-semibold transition-colors"
        >
          Back
        </button>
        {onSkip && (
          <button
            onClick={onSkip}
            className="px-6 py-3 bg-transparent border border-white/20 text-[#aaa] hover:text-[#e0e0e0] hover:border-white/30 rounded-lg font-semibold transition-colors"
          >
            Skip
          </button>
        )}
      </div>
    </div>
  );
}
