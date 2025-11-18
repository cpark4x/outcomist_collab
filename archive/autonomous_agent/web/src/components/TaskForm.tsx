/**
 * Task submission form component
 * Large textarea for goal, collapsible optional fields
 */

import { useState } from 'react';
import { ChevronDown, ChevronUp, Send } from 'lucide-react';
import { useCreateTask } from '../hooks/useTasks';
import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';

export function TaskForm() {
  const [goal, setGoal] = useState('');
  const [context, setContext] = useState('');
  const [constraints, setConstraints] = useState('');
  const [showOptional, setShowOptional] = useState(false);

  const navigate = useNavigate();
  const createTask = useCreateTask();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (goal.trim().length < 10) {
      alert('Goal must be at least 10 characters');
      return;
    }

    try {
      const task = await createTask.mutateAsync({
        goal: goal.trim(),
        context: context.trim() || undefined,
        constraints: constraints.trim()
          ? constraints.split('\n').filter(c => c.trim())
          : undefined,
      });

      // Navigate to task detail page
      navigate(`/tasks/${task.task_id}`);
    } catch (error) {
      console.error('Failed to create task:', error);
      alert('Failed to create task. Please try again.');
    }
  };

  const isValid = goal.trim().length >= 10;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Main goal input */}
      <div>
        <label htmlFor="goal" className="block text-sm font-medium text-gray-700 mb-2">
          What would you like the agent to do?
        </label>
        <textarea
          id="goal"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Describe your task in detail. The agent will plan, execute, and verify the work..."
          className={clsx(
            "w-full px-4 py-3 rounded-lg border",
            "focus:outline-none focus:ring-2 focus:ring-blue-500",
            "min-h-[150px] resize-y",
            "text-base",
            goal.trim() && goal.trim().length < 10 && "border-red-300"
          )}
          disabled={createTask.isPending}
        />
        <p className="mt-1 text-sm text-gray-500">
          {goal.length} characters (minimum 10)
        </p>
      </div>

      {/* Optional fields toggle */}
      <button
        type="button"
        onClick={() => setShowOptional(!showOptional)}
        className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
      >
        {showOptional ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        Optional: Add context or constraints
      </button>

      {/* Optional fields */}
      {showOptional && (
        <div className="space-y-4 pl-4 border-l-2 border-gray-200">
          <div>
            <label htmlFor="context" className="block text-sm font-medium text-gray-700 mb-2">
              Context (optional)
            </label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Any background information that might help the agent..."
              className="w-full px-4 py-3 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px] resize-y"
              disabled={createTask.isPending}
            />
          </div>

          <div>
            <label htmlFor="constraints" className="block text-sm font-medium text-gray-700 mb-2">
              Constraints (optional)
            </label>
            <textarea
              id="constraints"
              value={constraints}
              onChange={(e) => setConstraints(e.target.value)}
              placeholder="One constraint per line, e.g.:&#10;Must use Python 3.11+&#10;Keep response under 1000 words"
              className="w-full px-4 py-3 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px] resize-y"
              disabled={createTask.isPending}
            />
            <p className="mt-1 text-sm text-gray-500">
              One constraint per line
            </p>
          </div>
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={!isValid || createTask.isPending}
        className={clsx(
          "w-full flex items-center justify-center gap-2",
          "px-6 py-4 rounded-lg font-medium text-lg",
          "transition-colors",
          isValid && !createTask.isPending
            ? "bg-blue-600 text-white hover:bg-blue-700"
            : "bg-gray-300 text-gray-500 cursor-not-allowed"
        )}
      >
        {createTask.isPending ? (
          <>
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            Creating task...
          </>
        ) : (
          <>
            <Send size={20} />
            Delegate Task
          </>
        )}
      </button>
    </form>
  );
}
