import { ProjectStatus } from '../../types';

interface StatusBadgeProps {
  status: ProjectStatus;
  message?: string;
}

const statusConfig: Record<
  ProjectStatus,
  { label: string; color: string; bgGradient: string; border: string; pulse: boolean; callToAction: string }
> = {
  idle: {
    label: 'Idle',
    color: '#E5E7EB',
    bgGradient: 'rgba(75, 85, 99, 0.6)',
    border: '1px solid rgba(156, 163, 175, 0.8)',
    pulse: false,
    callToAction: 'Give me a task',
  },
  planning: {
    label: 'Planning',
    color: '#93C5FD',
    bgGradient: 'linear-gradient(135deg, rgba(74, 144, 226, 0.35), rgba(74, 144, 226, 0.25))',
    border: '1px solid rgba(74, 144, 226, 0.5)',
    pulse: true,
    callToAction: 'Analyzing your request...',
  },
  working: {
    label: 'Working',
    color: '#86EFAC',
    bgGradient: 'linear-gradient(135deg, rgba(80, 200, 120, 0.35), rgba(80, 200, 120, 0.25))',
    border: '1px solid rgba(80, 200, 120, 0.5)',
    pulse: true,
    callToAction: 'Creating deliverables...',
  },
  needs_input: {
    label: 'Needs Input',
    color: '#FDE047',
    bgGradient: 'linear-gradient(135deg, rgba(255, 193, 7, 0.35), rgba(255, 193, 7, 0.25))',
    border: '1px solid rgba(255, 193, 7, 0.5)',
    pulse: true,
    callToAction: 'Waiting for your response',
  },
  verifying: {
    label: 'Verifying',
    color: '#D8B4FE',
    bgGradient: 'linear-gradient(135deg, rgba(159, 122, 234, 0.35), rgba(159, 122, 234, 0.25))',
    border: '1px solid rgba(159, 122, 234, 0.5)',
    pulse: true,
    callToAction: 'Checking quality...',
  },
  complete: {
    label: 'Complete',
    color: '#86EFAC',
    bgGradient: 'linear-gradient(135deg, rgba(80, 200, 120, 0.35), rgba(80, 200, 120, 0.25))',
    border: '1px solid rgba(80, 200, 120, 0.5)',
    pulse: false,
    callToAction: 'Ready for review',
  },
};

export function StatusBadge({ status, message }: StatusBadgeProps) {
  const config = statusConfig[status];
  const displayMessage = message || config.callToAction;

  return (
    <div
      className="px-3 py-1 rounded-[14px] text-[11px] font-semibold flex items-center gap-1.5 uppercase tracking-wide cursor-help"
      style={{
        background: config.bgGradient,
        color: config.color,
        border: config.border,
      }}
      title={displayMessage}
    >
      <div
        className={`w-1.5 h-1.5 rounded-full ${
          config.pulse ? 'animate-pulse-status' : ''
        }`}
        style={{ background: config.color }}
      />
      {config.label}
    </div>
  );
}
