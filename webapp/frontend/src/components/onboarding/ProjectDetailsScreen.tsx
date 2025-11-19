import { useState } from 'react';
import type { ProjectType } from '../../types';

interface ProjectDetailsScreenProps {
  projectType: ProjectType;
  onSubmit: (name: string, description: string) => void;
  onBack: () => void;
}

const typeInfo: Record<ProjectType, { icon: string; title: string }> = {
  game: { icon: '🎮', title: 'Game' },
  trip: { icon: '✈️', title: 'Trip' },
  content: { icon: '✍️', title: 'Content' },
  presentation: { icon: '📊', title: 'Presentation' },
};

export function ProjectDetailsScreen({ projectType, onSubmit, onBack }: ProjectDetailsScreenProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onSubmit(name.trim(), description.trim());
    }
  };

  const info = typeInfo[projectType];

  return (
    <div className="bg-[rgba(42,42,42,0.6)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-12">
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">{info.icon}</div>
        <h2 className="text-3xl font-bold text-[#e0e0e0] mb-3">Name Your {info.title}</h2>
        <p className="text-[#aaa]">Give your project a name and optional description</p>
      </div>

      <form onSubmit={handleSubmit} className="max-w-md mx-auto mb-8">
        <div className="mb-6">
          <label htmlFor="name" className="block text-sm font-semibold text-[#ccc] mb-2">
            Project Name *
          </label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder={`My ${info.title}`}
            className="w-full px-4 py-3 bg-[rgba(30,30,30,0.5)] border border-white/10 rounded-lg text-[#e0e0e0] placeholder-[#666] focus:border-[#4A90E2] focus:outline-none transition-colors"
            required
            autoFocus
          />
        </div>

        <div className="mb-6">
          <label htmlFor="description" className="block text-sm font-semibold text-[#ccc] mb-2">
            Description (Optional)
          </label>
          <textarea
            id="description"
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="What do you want to create?"
            rows={4}
            className="w-full px-4 py-3 bg-[rgba(30,30,30,0.5)] border border-white/10 rounded-lg text-[#e0e0e0] placeholder-[#666] focus:border-[#4A90E2] focus:outline-none transition-colors resize-none"
          />
        </div>

        <div className="flex gap-4">
          <button
            type="button"
            onClick={onBack}
            className="flex-1 px-6 py-3 bg-transparent border border-white/20 text-[#aaa] hover:text-[#e0e0e0] hover:border-white/30 rounded-lg font-semibold transition-colors"
          >
            Back
          </button>
          <button
            type="submit"
            disabled={!name.trim()}
            className="flex-1 px-6 py-3 bg-[#4A90E2] hover:bg-[#357ABD] disabled:bg-[#333] disabled:text-[#666] text-white rounded-lg font-semibold transition-colors"
          >
            Create Project
          </button>
        </div>
      </form>
    </div>
  );
}
