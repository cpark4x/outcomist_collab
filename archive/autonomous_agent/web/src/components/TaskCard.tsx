/**
 * Task history card component
 * Shows task summary in list view
 */

import { Clock, CheckCircle, XCircle, Loader } from 'lucide-react';
import type { Task, TaskStatus } from '../types';
import { Link } from 'react-router-dom';
import clsx from 'clsx';

interface TaskCardProps {
  task: Task;
}

// Status display configuration
const STATUS_CONFIG: Record<TaskStatus, {
  label: string;
  icon: React.ElementType;
  color: string;
}> = {
  pending: { label: 'Pending', icon: Loader, color: 'text-gray-500' },
  planning: { label: 'Planning', icon: Loader, color: 'text-blue-500' },
  executing: { label: 'Executing', icon: Loader, color: 'text-blue-500' },
  verifying: { label: 'Verifying', icon: Loader, color: 'text-blue-500' },
  completed: { label: 'Completed', icon: CheckCircle, color: 'text-green-600' },
  failed: { label: 'Failed', icon: XCircle, color: 'text-red-600' },
};

export function TaskCard({ task }: TaskCardProps) {
  const config = STATUS_CONFIG[task.status];
  const Icon = config.icon;
  const isActive = ['pending', 'planning', 'executing', 'verifying'].includes(task.status);

  // Format timestamp
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <Link
      to={`/tasks/${task.task_id}`}
      className="block bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-md transition-all"
    >
      <div className="flex items-start justify-between gap-4">
        {/* Task info */}
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-gray-900 line-clamp-2 mb-2">
            {task.goal}
          </h3>

          {task.current_activity && isActive && (
            <p className="text-sm text-gray-600 line-clamp-1 mb-2">
              {task.current_activity}
            </p>
          )}

          <div className="flex items-center gap-3 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <Clock size={14} />
              {formatTime(task.updated_at)}
            </div>

            {task.elapsed_time !== undefined && isActive && (
              <span>• {Math.floor(task.elapsed_time / 60)}m {task.elapsed_time % 60}s</span>
            )}
          </div>
        </div>

        {/* Status badge */}
        <div className={clsx(
          "flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap",
          isActive ? "bg-blue-50 text-blue-700" :
          task.status === 'completed' ? "bg-green-50 text-green-700" :
          "bg-red-50 text-red-700"
        )}>
          <Icon size={16} className={isActive ? 'animate-spin' : ''} />
          {config.label}
        </div>
      </div>
    </Link>
  );
}
