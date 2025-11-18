/**
 * Manus-style progress indicator for AI work
 */

import { ProgressData } from '../../types';
import { getPhaseIcon, getPhaseGradient, getPhaseGlow } from '../../utils/progressHelpers';

interface ProgressIndicatorProps {
  progress: ProgressData;
}

export function ProgressIndicator({ progress }: ProgressIndicatorProps) {
  return (
    <div className="mt-2 space-y-1.5">
      {/* Progress Bar Container */}
      <div className="relative h-1 bg-white/[0.03] rounded-full overflow-hidden">
        {/* Animated Fill */}
        <div
          className="absolute inset-y-0 left-0 rounded-full transition-all duration-500 ease-[cubic-bezier(0.34,1.2,0.64,1)]"
          style={{
            width: `${progress.percentage}%`,
            background: getPhaseGradient(progress.phase),
            boxShadow: getPhaseGlow(progress.phase),
          }}
        />

        {/* Shimmer Effect */}
        <div
          className="absolute inset-0 opacity-30 shimmer-animation"
          style={{
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent)',
          }}
        />
      </div>

      {/* Status Text */}
      <div className="flex items-center justify-between text-[10px]">
        <div className="flex items-center gap-1.5">
          <span className="text-sm">{getPhaseIcon(progress.phase)}</span>
          <span className="text-[#aaa] font-medium">{progress.statusText}</span>
        </div>

        {progress.step && (
          <span className="text-[#666] font-mono">
            {progress.step.current}/{progress.step.total}
          </span>
        )}
      </div>
    </div>
  );
}
