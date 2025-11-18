import { useState } from 'react';
import type { ProjectType } from '../../types';

interface NewProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: { type: ProjectType; name: string; description: string }) => void;
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
    description: 'Interactive browser game',
  },
  {
    type: 'trip',
    icon: '✈️',
    title: 'Trip',
    description: 'Travel itinerary planner',
  },
  {
    type: 'content',
    icon: '✍️',
    title: 'Content',
    description: 'Written content',
  },
  {
    type: 'presentation',
    icon: '📊',
    title: 'Presentation',
    description: 'Slide deck',
  },
];

export function NewProjectModal({ isOpen, onClose, onSubmit }: NewProjectModalProps) {
  const handleTypeSelect = (type: ProjectType) => {
    // Auto-generate name based on type
    const names: Record<ProjectType, string> = {
      game: 'New Game',
      trip: 'New Trip',
      content: 'New Content',
      presentation: 'New Presentation',
    };

    onSubmit({
      type,
      name: names[type],
      description: '',
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-6">
      <div className="bg-[rgba(42,42,42,0.95)] backdrop-blur-[20px] border border-white/[0.08] rounded-2xl p-8 max-w-lg w-full">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-[#e0e0e0]">New Project</h2>
          <button
            onClick={onClose}
            className="text-[#888] hover:text-[#e0e0e0] text-2xl transition-colors"
          >
            ×
          </button>
        </div>

        <p className="text-[#888] mb-6 text-sm">Select a project type to get started</p>

        <div className="grid grid-cols-2 gap-4">
          {projectTypes.map(pt => (
            <button
              key={pt.type}
              onClick={() => handleTypeSelect(pt.type)}
              className="bg-[rgba(30,30,30,0.5)] border border-white/5 hover:border-[#4A90E2] hover:shadow-[0_0_20px_rgba(74,144,226,0.2)] rounded-xl p-6 text-center transition-all"
            >
              <div className="text-4xl mb-3">{pt.icon}</div>
              <div className="font-semibold text-[#e0e0e0] mb-1">{pt.title}</div>
              <div className="text-xs text-[#888]">{pt.description}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
