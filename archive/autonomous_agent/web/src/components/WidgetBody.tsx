/**
 * Autonomous Agent - Widget Body Component
 * Adaptive content area with log viewer and download buttons
 */

import React from 'react';
import type { AgentWidgetData } from '../types/widget';
import { LogViewer } from './LogViewer';
import { Download } from 'lucide-react';
import '../styles/WidgetBody.css';

interface WidgetBodyProps {
  widget: AgentWidgetData;
}

// Helper function to get user-friendly status message
const getStatusMessage = (status: string, logs: any[]): string => {
  if (status === 'running') {
    return 'Processing...';
  }

  if (logs.length > 0) {
    const lastLog = logs[logs.length - 1];
    const msg = lastLog.message.toLowerCase();

    if (msg.includes('completed') || msg.includes('done')) {
      return '✓ Done';
    }

    if (msg.includes('waiting') || msg.includes('ready') || msg.includes('initialized')) {
      return '⏸ Ready';
    }
  }

  if (status === 'idle') {
    return '⏸ Idle - Ready to start';
  }
  if (status === 'completed') {
    return '✓ Done';
  }
  if (status === 'paused') {
    return '⏸ Paused';
  }
  if (status === 'error') {
    return '⚠️ Error';
  }

  return status;
};

export const WidgetBody: React.FC<WidgetBodyProps> = ({ widget }) => {
  if (widget.state === 'minimized') {
    return (
      <div className="widget-body widget-body--minimized">
        <div className="widget-status-text">
          {getStatusMessage(widget.status, widget.logs)}
        </div>
      </div>
    );
  }

  if (widget.state === 'compact') {
    return (
      <div className="widget-body widget-body--compact">
        <div className="widget-summary">
          <div className="widget-summary-item">
            <span className="widget-summary-label">Status:</span>
            <span className="widget-summary-value">{getStatusMessage(widget.status, widget.logs)}</span>
          </div>
          <div className="widget-summary-item">
            <span className="widget-summary-label">Logs:</span>
            <span className="widget-summary-value">{widget.logs.length} entries</span>
          </div>
          {widget.taskResult && (
            <div className="widget-summary-item">
              <span className="widget-summary-label">Artifacts:</span>
              <span className="widget-summary-value">{widget.taskResult.artifacts.length} files</span>
            </div>
          )}
        </div>
        {widget.logs.length > 0 && (
          <div className="widget-last-log">
            {widget.logs[widget.logs.length - 1].message}
          </div>
        )}
      </div>
    );
  }

  // Expanded state
  return (
    <div className="widget-body widget-body--expanded">
      <LogViewer logs={widget.logs} />

      {/* Artifacts section */}
      {widget.taskResult && widget.taskResult.artifacts.length > 0 && (
        <div className="widget-artifacts">
          <div className="widget-artifacts-header">
            <span className="widget-artifacts-title">Artifacts ({widget.taskResult.artifacts.length})</span>
          </div>
          <div className="widget-artifacts-list">
            {widget.taskResult.artifacts.map((artifact: any, idx: number) => (
              <div key={idx} className="widget-artifact-item">
                <span className="widget-artifact-name">{artifact.name}</span>
                <button
                  className="widget-artifact-download"
                  onClick={() => {
                    const blob = new Blob([JSON.stringify(artifact.content, null, 2)], {
                      type: 'application/json',
                    });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = artifact.name;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                  title="Download artifact"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Verification section */}
      {widget.taskResult && (
        <div className="widget-verification">
          <div className="widget-verification-header">
            <span className="widget-verification-label">Verification</span>
            <span className="widget-verification-value">
              {(widget.taskResult.validation.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="widget-verification-bar">
            <div
              className="widget-verification-fill"
              style={{ width: `${widget.taskResult.validation.confidence * 100}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
};
