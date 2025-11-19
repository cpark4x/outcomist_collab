import { useState, useEffect } from 'react';

export type TaskState = 'pending' | 'active' | 'completed' | 'failed';

export interface Task {
  id: string;
  label: string;
  state: TaskState;
  startedAt?: number;
  completedAt?: number;
  statusMessage?: string; // Current activity description
}

interface TaskProgressCardProps {
  tasks: Task[];
  projectId: string;
}

export function TaskProgressCard({ tasks, projectId }: TaskProgressCardProps) {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [currentTime, setCurrentTime] = useState(Date.now());

  // Update timer every second for active tasks
  useEffect(() => {
    const hasActiveTasks = tasks.some(t => t.state === 'active');
    if (!hasActiveTasks) return;

    const interval = setInterval(() => {
      setCurrentTime(Date.now());
    }, 1000);

    return () => clearInterval(interval);
  }, [tasks]);

  const completedCount = tasks.filter(t => t.state === 'completed').length;
  const totalCount = tasks.length;
  const activeTask = tasks.find(t => t.state === 'active');
  const allComplete = completedCount === totalCount && totalCount > 0;

  // Don't show if no tasks
  if (tasks.length === 0) return null;

  // Calculate total duration when all complete
  const getTotalDuration = () => {
    if (!allComplete) return null;
    const firstTask = tasks.find(t => t.startedAt);
    const lastTask = [...tasks].reverse().find(t => t.completedAt);
    if (!firstTask?.startedAt || !lastTask?.completedAt) return null;
    const totalSeconds = Math.floor((lastTask.completedAt - firstTask.startedAt) / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  // Get elapsed time for active task
  const getActiveTaskTime = () => {
    if (!activeTask?.startedAt) return null;
    const elapsed = Math.floor((currentTime - activeTask.startedAt) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="border-b border-slate-700/50 bg-slate-800/40 backdrop-blur-sm">
      {/* Header - Shows current task when collapsed */}
      <div
        className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-slate-700/20 transition-colors"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        <div className="flex items-center gap-3 flex-1 min-w-0">
          {isCollapsed ? (
            allComplete ? (
              // Collapsed + Complete: Show completion summary
              <>
                <span className="text-green-400 text-sm flex-shrink-0">✓</span>
                <span className="text-sm text-slate-300">Complete</span>
                {getTotalDuration() && (
                  <span className="text-xs text-slate-400 font-mono flex-shrink-0">
                    {getTotalDuration()}
                  </span>
                )}
                <span className="text-xs text-slate-500 flex-shrink-0">
                  {totalCount}/{totalCount}
                </span>
              </>
            ) : activeTask ? (
              // Collapsed + Active: Show current activity + timer + counter
              <>
                <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse-status flex-shrink-0" />
                <span className="text-sm text-slate-300 truncate">
                  {activeTask.statusMessage || activeTask.label}
                </span>
                {getActiveTaskTime() && (
                  <span className="text-xs text-slate-400 font-mono flex-shrink-0">
                    {getActiveTaskTime()}
                  </span>
                )}
                <span className="text-xs text-slate-500 flex-shrink-0">
                  {completedCount + 1}/{totalCount}
                </span>
              </>
            ) : (
              // Collapsed + No active: Show progress only
              <>
                <span className="text-sm text-slate-300">Task progress</span>
                <span className="text-xs text-slate-500">
                  {completedCount}/{totalCount}
                </span>
              </>
            )
          ) : (
            // Expanded: Show "Task progress X / Y"
            <>
              <span className="text-sm font-semibold text-slate-200">Task progress</span>
              <span className="text-xs text-slate-400 font-medium">
                {completedCount} / {totalCount}
              </span>
            </>
          )}
        </div>
        <svg
          className={`w-4 h-4 text-slate-400 transition-transform flex-shrink-0 ${
            isCollapsed ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>

      {/* Task List - Collapsible */}
      {!isCollapsed && (
        <div className="px-4 pb-4 space-y-2">
          {tasks.map((task) => (
            <TaskItem key={task.id} task={task} currentTime={currentTime} />
          ))}
        </div>
      )}
    </div>
  );
}

interface TaskItemProps {
  task: Task;
  currentTime: number;
}

function TaskItem({ task, currentTime }: TaskItemProps) {
  const getElapsedTime = () => {
    if (!task.startedAt) return null;
    const elapsed = Math.floor((currentTime - task.startedAt) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const getDuration = () => {
    if (!task.startedAt || !task.completedAt) return null;
    const duration = Math.floor((task.completedAt - task.startedAt) / 1000);
    return `${duration}s`;
  };

  const getStateIcon = () => {
    switch (task.state) {
      case 'completed':
        return <span className="text-green-400 text-sm">✓</span>;
      case 'active':
        return (
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse-status" />
        );
      case 'failed':
        return <span className="text-red-400 text-sm">✗</span>;
      case 'pending':
      default:
        return (
          <svg className="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
          </svg>
        );
    }
  };

  return (
    <div className="flex items-center gap-3">
      <div className="flex-shrink-0 w-4 flex items-center justify-center">
        {getStateIcon()}
      </div>
      <div className="flex-1 min-w-0">
        <div className={`text-sm ${
          task.state === 'completed'
            ? 'text-slate-400'
            : task.state === 'active'
            ? 'text-slate-200 font-medium'
            : 'text-slate-500'
        }`}>
          {task.label}
        </div>
        {task.state === 'active' && (
          <div className="text-xs text-slate-400 mt-0.5">
            {getElapsedTime()}
            {task.statusMessage && (
              <span className="text-slate-500 ml-2">{task.statusMessage}</span>
            )}
          </div>
        )}
        {task.state === 'completed' && getDuration() && (
          <div className="text-xs text-slate-600 mt-0.5">
            {getDuration()}
          </div>
        )}
      </div>
    </div>
  );
}
