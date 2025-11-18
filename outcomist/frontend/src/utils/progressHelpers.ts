/**
 * Progress indication helpers for Manus-style status updates
 */

export type ProgressPhase = 'understanding' | 'planning' | 'thinking' | 'generating' | 'tool_use' | 'complete';

export interface ProgressData {
  phase: ProgressPhase;
  percentage: number;
  statusText: string;
  step?: {
    current: number;
    total: number;
  };
  startTime: Date;
  filename?: string;
}

export function getPhaseIcon(phase: ProgressPhase): string {
  const icons = {
    understanding: '🤔',
    planning: '📝',
    thinking: '💭',
    generating: '✨',
    tool_use: '🛠️',
    complete: '✓',
  };
  return icons[phase] || '●';
}

export function getPhaseGradient(phase: ProgressPhase): string {
  const gradients = {
    understanding: 'linear-gradient(90deg, #4A90E2 0%, #667eea 100%)',
    planning: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
    thinking: 'linear-gradient(90deg, #764ba2 0%, #667eea 100%)',
    generating: 'linear-gradient(90deg, #4A90E2 0%, #667eea 100%)',
    tool_use: 'linear-gradient(90deg, #764ba2 0%, #4A90E2 100%)',
    complete: 'linear-gradient(90deg, #10b981 0%, #34d399 100%)',
  };
  return gradients[phase];
}

export function getPhaseGlow(phase: ProgressPhase): string {
  const glows = {
    understanding: '0 0 8px rgba(74, 144, 226, 0.3)',
    planning: '0 0 8px rgba(102, 126, 234, 0.3)',
    thinking: '0 0 8px rgba(118, 75, 162, 0.3)',
    generating: '0 0 8px rgba(74, 144, 226, 0.3)',
    tool_use: '0 0 8px rgba(118, 75, 162, 0.3)',
    complete: '0 0 8px rgba(16, 185, 129, 0.3)',
  };
  return glows[phase];
}

export function getPhaseColor(phase: ProgressPhase, alpha: number): string {
  const colors = {
    understanding: `rgba(74, 144, 226, ${alpha})`,
    planning: `rgba(102, 126, 234, ${alpha})`,
    thinking: `rgba(118, 75, 162, ${alpha})`,
    generating: `rgba(74, 144, 226, ${alpha})`,
    tool_use: `rgba(118, 75, 162, ${alpha})`,
    complete: `rgba(16, 185, 129, ${alpha})`,
  };
  return colors[phase];
}

export function formatElapsedTime(startTime: Date): string {
  const elapsed = Date.now() - startTime.getTime();
  const minutes = Math.floor(elapsed / 60000);
  const seconds = Math.floor((elapsed % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

export function getPhaseLabel(phase: ProgressPhase, filename?: string): string {
  const labels = {
    understanding: 'Understanding your request...',
    planning: 'Planning approach...',
    thinking: 'Thinking through options...',
    generating: 'Crafting response...',
    tool_use: filename ? `Creating ${filename}...` : 'Creating files...',
    complete: 'Complete',
  };
  return labels[phase];
}
