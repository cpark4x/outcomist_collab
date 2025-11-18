import { ProjectStatus } from '../../types';

interface StatusBadgeProps {
  status: ProjectStatus;
}

const statusConfig: Record<
  ProjectStatus,
  { label: string; color: string; bgGradient: string; border: string }
> = {
  active: {
    label: 'Active',
    color: '#66D98F',
    bgGradient: 'linear-gradient(135deg, rgba(80, 200, 120, 0.2), rgba(80, 200, 120, 0.15))',
    border: '1px solid rgba(80, 200, 120, 0.3)',
  },
  running: {
    label: 'Running',
    color: '#6BA3E8',
    bgGradient: 'linear-gradient(135deg, rgba(74, 144, 226, 0.2), rgba(74, 144, 226, 0.15))',
    border: '1px solid rgba(74, 144, 226, 0.3)',
  },
  waiting: {
    label: 'Needs Input',
    color: '#FFD54F',
    bgGradient: 'linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(255, 193, 7, 0.15))',
    border: '1px solid rgba(255, 193, 7, 0.3)',
  },
  complete: {
    label: 'Complete',
    color: '#66D98F',
    bgGradient: 'linear-gradient(135deg, rgba(80, 200, 120, 0.2), rgba(80, 200, 120, 0.15))',
    border: '1px solid rgba(80, 200, 120, 0.3)',
  },
  idle: {
    label: 'Idle',
    color: '#999',
    bgGradient: 'rgba(136, 136, 136, 0.15)',
    border: '1px solid rgba(136, 136, 136, 0.2)',
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <div
      className="px-3 py-1 rounded-[14px] text-[11px] font-semibold flex items-center gap-1.5 uppercase tracking-wide"
      style={{
        background: config.bgGradient,
        color: config.color,
        border: config.border,
      }}
    >
      <div
        className={`w-1.5 h-1.5 rounded-full ${
          status === 'running' ? 'animate-pulse-status' : ''
        }`}
        style={{ background: config.color }}
      />
      {config.label}
    </div>
  );
}
