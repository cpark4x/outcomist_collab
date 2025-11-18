/**
 * Results display component
 * Shows artifacts, verification badge, and details
 */

import { CheckCircle, XCircle, Download, AlertCircle, Copy } from 'lucide-react';
import type { TaskResult } from '../types';
import { useDownloadArtifact } from '../hooks/useTasks';
import { useState } from 'react';
import clsx from 'clsx';

interface ResultsViewProps {
  taskId: string;
  result: TaskResult;
}

export function ResultsView({ taskId, result }: ResultsViewProps) {
  const [expandedChecks, setExpandedChecks] = useState(false);
  const downloadArtifact = useDownloadArtifact();

  const handleDownload = (artifactPath: string) => {
    downloadArtifact.mutate({ taskId, artifactPath });
  };

  const confidenceColor =
    result.validation.overall_confidence >= 80 ? 'green' :
    result.validation.overall_confidence >= 60 ? 'yellow' :
    'red';

  const confidenceColorClasses = {
    green: 'bg-green-100 text-green-800 border-green-200',
    yellow: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    red: 'bg-red-100 text-red-800 border-red-200',
  };

  return (
    <div className="space-y-6">
      {/* Verification badge */}
      <div className={clsx(
        "p-6 rounded-lg border-2",
        result.success
          ? confidenceColorClasses[confidenceColor]
          : "bg-red-50 border-red-300 text-red-900"
      )}>
        <div className="flex items-start gap-4">
          {result.success ? (
            <CheckCircle size={32} className="flex-shrink-0" />
          ) : (
            <XCircle size={32} className="flex-shrink-0" />
          )}

          <div className="flex-1">
            <h3 className="text-lg font-semibold mb-2">
              {result.success ? 'Task Completed' : 'Task Failed'}
            </h3>

            {result.success ? (
              <>
                <p className="text-sm mb-3">
                  Verification confidence: {result.validation.overall_confidence}%
                </p>

                <div className="flex gap-2 text-sm">
                  <span>
                    {result.validation.checks.filter(c => c.passed).length} of{' '}
                    {result.validation.checks.length} checks passed
                  </span>
                </div>
              </>
            ) : (
              <p className="text-sm">{result.error_message || 'An error occurred'}</p>
            )}
          </div>
        </div>
      </div>

      {/* Artifacts list */}
      {result.artifacts.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Artifacts</h3>

          <div className="space-y-2">
            {result.artifacts.map((artifact, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 truncate">
                    {artifact.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {artifact.type}
                    {artifact.size && ` • ${(artifact.size / 1024).toFixed(1)} KB`}
                  </p>
                </div>

                <button
                  onClick={() => handleDownload(artifact.path)}
                  disabled={downloadArtifact.isPending}
                  className="ml-4 flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                  <Download size={16} />
                  Download
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Verification checks */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <button
          onClick={() => setExpandedChecks(!expandedChecks)}
          className="w-full flex items-center justify-between text-left"
        >
          <h3 className="text-lg font-medium text-gray-900">
            Verification Details
          </h3>
          <span className="text-sm text-gray-500">
            {expandedChecks ? 'Hide' : 'Show'}
          </span>
        </button>

        {expandedChecks && (
          <div className="mt-4 space-y-3">
            {result.validation.checks.map((check, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
              >
                {check.passed ? (
                  <CheckCircle size={20} className="flex-shrink-0 text-green-600 mt-0.5" />
                ) : (
                  <XCircle size={20} className="flex-shrink-0 text-red-600 mt-0.5" />
                )}

                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900">{check.check}</p>
                  {check.details && (
                    <p className="text-sm text-gray-600 mt-1">{check.details}</p>
                  )}
                </div>
              </div>
            ))}

            {/* Issues */}
            {result.validation.issues.length > 0 && (
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertCircle size={20} className="flex-shrink-0 text-yellow-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-yellow-900 mb-2">Issues Found</p>
                    <ul className="space-y-1">
                      {result.validation.issues.map((issue, index) => (
                        <li key={index} className="text-sm text-yellow-800">
                          • {issue}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Use as template button */}
      <button
        onClick={() => {
          // Copy task goal to clipboard for reuse
          navigator.clipboard.writeText(result.task_id);
          alert('Task ID copied! You can reference this task when creating similar ones.');
        }}
        className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
      >
        <Copy size={20} />
        Use as Template
      </button>
    </div>
  );
}
