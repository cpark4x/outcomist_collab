/**
 * Main dashboard view
 * Task submission form and task history list
 */

import { useState } from 'react';
import { TaskForm } from '../components/TaskForm';
import { TaskCard } from '../components/TaskCard';
import { useTasks } from '../hooks/useTasks';
import type { TaskStatus } from '../types';
import clsx from 'clsx';
import { Loader, AlertCircle } from 'lucide-react';

type FilterStatus = 'all' | TaskStatus;

export function Dashboard() {
  const [filter, setFilter] = useState<FilterStatus>('all');
  const { data, isLoading, error } = useTasks();

  // Filter tasks by status
  const filteredTasks = data?.tasks.filter(task =>
    filter === 'all' || task.status === filter
  ) || [];

  // Status filter tabs
  const filters: { key: FilterStatus; label: string }[] = [
    { key: 'all', label: 'All' },
    { key: 'completed', label: 'Completed' },
    { key: 'pending', label: 'In Progress' },
    { key: 'failed', label: 'Failed' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Autonomous Agent</h1>
          <p className="text-gray-600 mt-2">
            Delegate tasks to the AI agent and monitor their progress
          </p>
        </div>

        {/* Task submission form */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">New Task</h2>
          <TaskForm />
        </div>

        {/* Task history */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Task History</h2>

          {/* Status filters */}
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
            {filters.map(({ key, label }) => {
              const count = key === 'all'
                ? data?.tasks.length
                : data?.tasks.filter(t => t.status === key).length;

              return (
                <button
                  key={key}
                  onClick={() => setFilter(key)}
                  className={clsx(
                    "px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap transition-colors",
                    filter === key
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {label}
                  {count !== undefined && count > 0 && (
                    <span className="ml-2 opacity-75">({count})</span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Task list */}
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader className="animate-spin text-blue-600" size={32} />
            </div>
          ) : error ? (
            <div className="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
              <AlertCircle size={20} />
              <span>Failed to load tasks. Please refresh the page.</span>
            </div>
          ) : filteredTasks.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              {filter === 'all'
                ? 'No tasks yet. Create your first task above!'
                : `No ${filter} tasks found.`}
            </div>
          ) : (
            <div className="space-y-3">
              {filteredTasks.map(task => (
                <TaskCard key={task.task_id} task={task} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
