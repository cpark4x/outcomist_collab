/**
 * Task detail view
 * Shows progress and results for a specific task
 */

import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Loader, AlertCircle } from 'lucide-react';
import { useTask, useTaskResult } from '../hooks/useTasks';
import { ProgressView } from '../components/ProgressView';
import { ResultsView } from '../components/ResultsView';

export function TaskDetail() {
  const { taskId } = useParams<{ taskId: string }>();
  const { data: task, isLoading: taskLoading, error: taskError } = useTask(taskId!);
  const { data: result, isLoading: resultLoading, error: resultError } = useTaskResult(
    taskId!,
    task?.status === 'completed' || task?.status === 'failed'
  );

  if (taskLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader className="animate-spin text-blue-600" size={48} />
      </div>
    );
  }

  if (taskError || !task) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full mx-4">
          <div className="bg-white rounded-lg border border-red-200 p-6">
            <div className="flex items-center gap-3 text-red-800 mb-4">
              <AlertCircle size={24} />
              <h2 className="text-xl font-semibold">Task Not Found</h2>
            </div>
            <p className="text-gray-600 mb-4">
              The task you're looking for doesn't exist or couldn't be loaded.
            </p>
            <Link
              to="/"
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <ArrowLeft size={16} />
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const isActive = ['pending', 'planning', 'executing', 'verifying'].includes(task.status);
  const showResults = (task.status === 'completed' || task.status === 'failed') && result;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {/* Header with back button */}
        <div>
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft size={20} />
            Back to Dashboard
          </Link>

          <h1 className="text-2xl font-bold text-gray-900 mb-2">{task.goal}</h1>

          {task.context && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mt-4">
              <h2 className="text-sm font-medium text-gray-700 mb-2">Context</h2>
              <p className="text-gray-600">{task.context}</p>
            </div>
          )}

          {task.constraints && task.constraints.length > 0 && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mt-4">
              <h2 className="text-sm font-medium text-gray-700 mb-2">Constraints</h2>
              <ul className="space-y-1">
                {task.constraints.map((constraint, index) => (
                  <li key={index} className="text-gray-600 text-sm">
                    • {constraint}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Progress view for active tasks */}
        {isActive && <ProgressView task={task} />}

        {/* Results view for completed/failed tasks */}
        {showResults && !resultLoading && (
          <ResultsView taskId={task.task_id} result={result} />
        )}

        {/* Loading results */}
        {showResults && resultLoading && (
          <div className="bg-white rounded-lg border border-gray-200 p-12 flex items-center justify-center">
            <Loader className="animate-spin text-blue-600" size={32} />
          </div>
        )}

        {/* Results error */}
        {showResults && resultError && (
          <div className="bg-white rounded-lg border border-red-200 p-6">
            <div className="flex items-center gap-3 text-red-800">
              <AlertCircle size={24} />
              <div>
                <h3 className="font-semibold">Failed to Load Results</h3>
                <p className="text-sm text-gray-600 mt-1">
                  There was an error loading the task results. Please try again.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
