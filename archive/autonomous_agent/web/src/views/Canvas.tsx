/**
 * Autonomous Agent - Canvas View
 * Widget-based canvas workspace for autonomous agent tasks
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { AgentWidget } from '../components/AgentWidget';
import { useCanvasState } from '../hooks/useCanvasState';
import { createWidget } from '../utils/widgetFactory';
import { api } from '../api/client';
import { Plus } from 'lucide-react';
import '../styles/Canvas.css';

export default function Canvas() {
  const {
    canvasState,
    addWidget,
    removeWidget,
    updateWidget,
    selectWidget,
    bringToFront,
    changeWidgetState,
    setCanvasPan,
    setCanvasScale,
  } = useCanvasState();

  const canvasRef = useRef<HTMLDivElement>(null);
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const [showNewTaskModal, setShowNewTaskModal] = useState(false);
  const [newTaskGoal, setNewTaskGoal] = useState('');

  // Save canvas state to localStorage on changes
  useEffect(() => {
    const widgets = Array.from(canvasState.widgets.values());
    const state = {
      widgets,
      scale: canvasState.scale,
      pan: canvasState.pan,
    };
    localStorage.setItem('canvas-state', JSON.stringify(state));
  }, [canvasState]);

  // Handle creating new agent widget with task
  const handleCreateWidget = useCallback(async () => {
    if (!newTaskGoal.trim()) return;

    try {
      // Submit task to backend
      const response = await api.createTask({ goal: newTaskGoal });

      // Calculate position for new widget
      const widgetCount = canvasState.widgets.size;
      const position = {
        x: 100 + (widgetCount % 4) * 350,
        y: 100 + Math.floor(widgetCount / 4) * 220,
      };

      // Create widget with task ID
      const newWidget = createWidget({
        name: `Task ${widgetCount + 1}`,
        type: 'agent',
        status: 'running',
        position,
      });

      // Add widget with task ID
      addWidget({
        ...newWidget,
        taskId: response.task_id,
        logs: [
          {
            timestamp: Date.now(),
            level: 'info',
            message: `Task submitted: ${newTaskGoal}`,
          },
          {
            timestamp: Date.now(),
            level: 'info',
            message: `Task ID: ${response.task_id}`,
          },
        ],
      });

      setNewTaskGoal('');
      setShowNewTaskModal(false);
    } catch (error) {
      console.error('Failed to create task:', error);
      alert('Failed to create task. Please check the backend connection.');
    }
  }, [newTaskGoal, canvasState.widgets.size, addWidget]);

  // Canvas panning
  const handleCanvasMouseDown = useCallback((e: React.MouseEvent) => {
    // Pan with middle mouse button or space+left click
    if (e.button === 1 || (e.button === 0 && e.shiftKey)) {
      e.preventDefault();
      setIsPanning(true);
      setPanStart({ x: e.clientX - canvasState.pan.x, y: e.clientY - canvasState.pan.y });
    }
  }, [canvasState.pan]);

  useEffect(() => {
    if (!isPanning) return;

    const handleMouseMove = (e: MouseEvent) => {
      requestAnimationFrame(() => {
        setCanvasPan({
          x: e.clientX - panStart.x,
          y: e.clientY - panStart.y,
        });
      });
    };

    const handleMouseUp = () => {
      setIsPanning(false);
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isPanning, panStart, setCanvasPan]);

  // Wheel zoom
  const handleWheel = useCallback((e: React.WheelEvent) => {
    const target = e.target as HTMLElement;
    const isOnWidget = target.closest('.agent-widget');

    // Zoom with Ctrl/Cmd + scroll
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      const newScale = Math.max(0.1, Math.min(3, canvasState.scale + delta));
      setCanvasScale(newScale);
      return;
    }

    // 2-finger trackpad pan (only when not on a widget)
    if (!isOnWidget && (Math.abs(e.deltaX) > 0 || Math.abs(e.deltaY) > 0)) {
      e.preventDefault();
      setCanvasPan({
        x: canvasState.pan.x - e.deltaX,
        y: canvasState.pan.y - e.deltaY,
      });
    }
  }, [canvasState.scale, canvasState.pan, setCanvasScale, setCanvasPan]);

  const handleCanvasClick = useCallback((e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      selectWidget(null);
    }
  }, [selectWidget]);

  const handleZoomIn = useCallback(() => {
    setCanvasScale(Math.min(3, canvasState.scale + 0.1));
  }, [canvasState.scale, setCanvasScale]);

  const handleZoomOut = useCallback(() => {
    setCanvasScale(Math.max(0.1, canvasState.scale - 0.1));
  }, [canvasState.scale, setCanvasScale]);

  const handleZoomReset = useCallback(() => {
    setCanvasScale(1);
    setCanvasPan({ x: 0, y: 0 });
  }, [setCanvasScale, setCanvasPan]);

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 overflow-hidden">
      {/* Grid pattern background */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `
              linear-gradient(rgba(100,200,255,0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(100,200,255,0.1) 1px, transparent 1px)
            `,
            backgroundSize: '40px 40px',
          }}
        />
      </div>

      {/* Top toolbar */}
      <div className="absolute top-0 left-0 right-0 h-16 bg-gradient-to-r from-slate-900/95 to-slate-800/95 backdrop-blur-md border-b border-slate-700/50 shadow-xl flex items-center justify-between px-8 z-10">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">A</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-white tracking-tight">Autonomous Agent</h1>
              <span className="text-xs text-slate-400">Canvas Workspace</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span>Widgets: {canvasState.widgets.size}</span>
            <span>|</span>
            <span>Zoom: {(canvasState.scale * 100).toFixed(0)}%</span>
          </div>

          <button
            onClick={() => setShowNewTaskModal(true)}
            className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-blue-500/50 font-medium"
          >
            <Plus className="w-5 h-5" />
            New Task
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={handleZoomOut}
              className="px-3 py-2 bg-slate-700/80 hover:bg-slate-600 text-white rounded-lg transition-all"
              title="Zoom out (Ctrl+Scroll)"
            >
              -
            </button>
            <button
              onClick={handleZoomReset}
              className="px-3 py-2 bg-slate-700/80 hover:bg-slate-600 text-white rounded-lg transition-all"
              title="Reset zoom"
            >
              Reset
            </button>
            <button
              onClick={handleZoomIn}
              className="px-3 py-2 bg-slate-700/80 hover:bg-slate-600 text-white rounded-lg transition-all"
              title="Zoom in (Ctrl+Scroll)"
            >
              +
            </button>
          </div>
        </div>
      </div>

      {/* Canvas area */}
      <div
        className="canvas-container pt-16 w-full h-full"
        onClick={handleCanvasClick}
        onMouseDown={handleCanvasMouseDown}
        onWheel={handleWheel}
        style={{ cursor: isPanning ? 'grabbing' : 'default' }}
      >
        <div
          ref={canvasRef}
          className={`canvas ${isPanning ? 'canvas--panning' : ''}`}
          style={{
            transform: `translate(${canvasState.pan.x}px, ${canvasState.pan.y}px) scale(${canvasState.scale})`,
          }}
        >
          {Array.from(canvasState.widgets.values()).map((widget) => (
            <AgentWidget
              key={widget.id}
              widget={widget}
              isSelected={canvasState.selectedWidgetId === widget.id}
              onSelect={selectWidget}
              onUpdate={updateWidget}
              onStateChange={changeWidgetState}
              onBringToFront={bringToFront}
              onClose={removeWidget}
            />
          ))}
        </div>
      </div>

      {/* New task modal */}
      {showNewTaskModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50 animate-in fade-in duration-200">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 w-full max-w-2xl mx-4 border border-slate-700/50 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">Create New Task</h2>

            <textarea
              value={newTaskGoal}
              onChange={(e) => setNewTaskGoal(e.target.value)}
              placeholder="What do you need done? Describe your goal in natural language..."
              className="w-full h-40 px-4 py-3 bg-slate-900/80 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
              autoFocus
            />

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleCreateWidget}
                disabled={!newTaskGoal.trim()}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white rounded-xl transition-all duration-200 shadow-lg disabled:shadow-none hover:shadow-blue-500/50 font-medium"
              >
                Create Task
              </button>
              <button
                onClick={() => {
                  setShowNewTaskModal(false);
                  setNewTaskGoal('');
                }}
                className="px-6 py-3 bg-slate-700/80 hover:bg-slate-600 text-white rounded-xl transition-all duration-200 font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Empty state */}
      {canvasState.widgets.size === 0 && (
        <div className="absolute inset-0 flex items-center justify-center pt-16">
          <div className="text-center max-w-md">
            <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-600/20 flex items-center justify-center">
              <Plus className="w-10 h-10 text-blue-400" />
            </div>
            <h2 className="text-3xl font-bold text-white mb-3">Your Canvas Awaits</h2>
            <p className="text-slate-400 mb-8 text-lg">Delegate your first task and watch it come to life</p>
            <button
              onClick={() => setShowNewTaskModal(true)}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl transition-all duration-200 shadow-lg hover:shadow-blue-500/50 font-medium text-lg"
            >
              Create Your First Task
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
