/**
 * Progress monitor component
 * Shows pipeline stages and current activity
 */

import { CheckCircle, Circle, Clock } from 'lucide-react';
import type { Task } from '../types';
import clsx from 'clsx';

interface ProgressViewProps {
  task: Task;
}

// Pipeline stages in order
const STAGES = [
  { key: 'planning', label: 'Planning' },
  { key: 'executing', label: 'Executing' },
  { key: 'verifying', label: 'Verifying' },
] as const;

export function ProgressView({ task }: ProgressViewProps) {
  const currentStageIndex = STAGES.findIndex(s => s.key === task.status);
  const isCompleted = task.status === 'completed';
  const isFailed = task.status === 'failed';

  // Format elapsed time
  const formatElapsedTime = (seconds?: number) => {
    if (!seconds) return '0s';
    if (seconds < 60) return `${seconds}s`;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-6">
      {/* Pipeline stages */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">Progress</h3>

        <div className="space-y-3">
          {STAGES.map((stage, index) => {
            const isPast = index < currentStageIndex;
            const isCurrent = index === currentStageIndex;

            return (
              <div key={stage.key} className="flex items-center gap-3">
                {/* Stage icon */}
                <div className={clsx(
                  "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                  isPast || (isCompleted && index === STAGES.length - 1)
                    ? "bg-green-100 text-green-600"
                    : isCurrent
                    ? "bg-blue-100 text-blue-600"
                    : "bg-gray-100 text-gray-400"
                )}>
                  {isPast || (isCompleted && index === STAGES.length - 1) ? (
                    <CheckCircle size={20} />
                  ) : isCurrent ? (
                    <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse" />
                  ) : (
                    <Circle size={20} />
                  )}
                </div>

                {/* Stage label */}
                <div className="flex-1">
                  <div className={clsx(
                    "font-medium",
                    isCurrent ? "text-gray-900" : "text-gray-600"
                  )}>
                    {stage.label}
                  </div>

                  {/* Current activity */}
                  {isCurrent && task.current_activity && (
                    <div className="text-sm text-gray-500 mt-1">
                      {task.current_activity}
                    </div>
                  )}
                </div>

                {/* Status indicator */}
                {isCurrent && !isFailed && (
                  <div className="text-sm text-blue-600 flex items-center gap-1">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" />
                    In progress
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Status messages */}
      {isFailed && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800 font-medium">Task failed</p>
          <p className="text-sm text-red-600 mt-1">
            {task.current_activity || 'An error occurred during execution'}
          </p>
        </div>
      )}

      {isCompleted && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-800 font-medium">Task completed successfully</p>
        </div>
      )}

      {/* Elapsed time */}
      {task.elapsed_time !== undefined && (
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Clock size={16} />
          <span>Elapsed time: {formatElapsedTime(task.elapsed_time)}</span>
        </div>
      )}
    </div>
  );
}
