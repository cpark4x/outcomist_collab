/**
 * Autonomous Agent - AgentWidget Component
 * Main widget component with dragging, resizing, and task status
 */

import React, { useCallback, useRef, useState, useEffect } from 'react';
import type { AgentWidgetData, WidgetState, DragState, ResizeState, ResizeHandle } from '../types/widget';
import { WidgetHeader } from './WidgetHeader';
import { WidgetBody } from './WidgetBody';
import { api } from '../api/client';
import '../styles/AgentWidget.css';

interface AgentWidgetProps {
  widget: AgentWidgetData;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onUpdate: (id: string, updates: Partial<AgentWidgetData>) => void;
  onStateChange: (id: string, state: WidgetState) => void;
  onBringToFront: (id: string) => void;
  onClose: (id: string) => void;
}

export const AgentWidget: React.FC<AgentWidgetProps> = ({
  widget,
  isSelected,
  onSelect,
  onUpdate,
  onStateChange,
  onBringToFront,
  onClose,
}) => {
  const widgetRef = useRef<HTMLDivElement>(null);
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false,
    startX: 0,
    startY: 0,
    offsetX: 0,
    offsetY: 0,
  });
  const [dragTransform, setDragTransform] = useState({ x: 0, y: 0 });
  const dragTransformRef = useRef({ x: 0, y: 0 });
  const [resizeState, setResizeState] = useState<ResizeState>({
    isResizing: false,
    handle: null,
    startX: 0,
    startY: 0,
    startWidth: 0,
    startHeight: 0,
  });
  const resizeStartPosRef = useRef({ x: 0, y: 0 });

  // Task polling - update status every 2 seconds
  useEffect(() => {
    if (!widget.taskId || widget.status === 'completed' || widget.status === 'error') {
      return;
    }

    const interval = setInterval(async () => {
      try {
        const task = await api.getTask(widget.taskId!);

        // Map backend status to widget status
        let widgetStatus = widget.status;
        if (task.status === 'completed') {
          widgetStatus = 'completed';
        } else if (task.status === 'failed') {
          widgetStatus = 'error';
        } else if (task.status === 'planning' || task.status === 'executing' || task.status === 'verifying') {
          widgetStatus = 'running';
        }

        // Add progress as log entry if changed
        const logs = [...widget.logs];
        if (task.progress && (!logs.length || logs[logs.length - 1].message !== task.progress)) {
          logs.push({
            timestamp: Date.now(),
            level: 'info',
            message: task.progress,
          });
        }

        onUpdate(widget.id, {
          status: widgetStatus,
          logs,
        });

        // If completed, fetch result
        if (task.status === 'completed') {
          const result = await api.getTaskResult(widget.taskId!);
          logs.push({
            timestamp: Date.now(),
            level: 'success',
            message: `Task completed! Generated ${result.artifacts.length} artifacts.`,
          });
          onUpdate(widget.id, {
            logs,
            taskResult: result,
          });
        }
      } catch (error) {
        console.error('Failed to poll task status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [widget.taskId, widget.status, widget.id, onUpdate]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button !== 0) return; // Only left click

    onSelect(widget.id);
    onBringToFront(widget.id);

    setDragState({
      isDragging: true,
      startX: e.clientX,
      startY: e.clientY,
      offsetX: widget.position.x,
      offsetY: widget.position.y,
    });
  }, [widget.id, widget.position, onSelect, onBringToFront]);

  const handleDoubleClick = useCallback(() => {
    const nextState: WidgetState = widget.state === 'expanded' ? 'compact' : 'expanded';
    onStateChange(widget.id, nextState);
  }, [widget.id, widget.state, onStateChange]);

  // Handle drag
  useEffect(() => {
    if (!dragState.isDragging) return;

    let rafId: number | null = null;

    const handleMouseMove = (e: MouseEvent) => {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }

      rafId = requestAnimationFrame(() => {
        const dx = e.clientX - dragState.startX;
        const dy = e.clientY - dragState.startY;

        const newX = dragState.offsetX + dx;
        const newY = dragState.offsetY + dy;

        const transformX = newX - widget.position.x;
        const transformY = newY - widget.position.y;
        dragTransformRef.current = { x: transformX, y: transformY };
        setDragTransform({ x: transformX, y: transformY });

        rafId = null;
      });
    };

    const handleMouseUp = () => {
      const dx = dragTransformRef.current.x;
      const dy = dragTransformRef.current.y;

      if (dx !== 0 || dy !== 0) {
        onUpdate(widget.id, {
          position: {
            x: widget.position.x + dx,
            y: widget.position.y + dy,
          },
        });
      }

      setDragState((prev) => ({ ...prev, isDragging: false }));
      setDragTransform({ x: 0, y: 0 });
      dragTransformRef.current = { x: 0, y: 0 };
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragState, widget.id, widget.position, onUpdate]);

  // Handle resize
  useEffect(() => {
    if (!resizeState.isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      const dx = e.clientX - resizeState.startX;
      const dy = e.clientY - resizeState.startY;

      let newWidth = resizeState.startWidth;
      let newHeight = resizeState.startHeight;
      let newX = resizeStartPosRef.current.x;
      let newY = resizeStartPosRef.current.y;

      const handle = resizeState.handle;
      if (handle?.includes('e')) newWidth += dx;
      if (handle?.includes('w')) {
        newWidth -= dx;
        newX += dx;
      }
      if (handle?.includes('s')) newHeight += dy;
      if (handle?.includes('n')) {
        newHeight -= dy;
        newY += dy;
      }

      const updates: Partial<AgentWidgetData> = {
        size: { width: Math.max(200, newWidth), height: Math.max(100, newHeight) },
      };

      if (newX !== resizeStartPosRef.current.x || newY !== resizeStartPosRef.current.y) {
        updates.position = { x: newX, y: newY };
      }

      onUpdate(widget.id, updates);
    };

    const handleMouseUp = () => {
      setResizeState((prev) => ({ ...prev, isResizing: false, handle: null }));
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [resizeState, widget.id, onUpdate]);

  const handleResizeStart = useCallback(
    (handle: ResizeHandle, e: React.MouseEvent) => {
      e.stopPropagation();
      resizeStartPosRef.current = { x: widget.position.x, y: widget.position.y };
      setResizeState({
        isResizing: true,
        handle,
        startX: e.clientX,
        startY: e.clientY,
        startWidth: widget.size.width,
        startHeight: widget.size.height,
      });
      onBringToFront(widget.id);
    },
    [widget, onBringToFront]
  );

  const handleRename = useCallback(
    (newName: string) => {
      onUpdate(widget.id, { name: newName });
    },
    [widget.id, onUpdate]
  );

  const handleWidgetClick = useCallback((e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    if (
      target.closest('.widget-header') ||
      target.closest('.widget-command-input') ||
      target.closest('.resize-handle')
    ) {
      return;
    }
    onSelect(widget.id);
  }, [widget.id, onSelect]);

  const widgetClasses = [
    'agent-widget',
    `agent-widget--${widget.state}`,
    `agent-widget--${widget.status}`,
    isSelected ? 'agent-widget--selected' : '',
    dragState.isDragging ? 'agent-widget--dragging' : '',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      ref={widgetRef}
      className={widgetClasses}
      style={{
        position: 'absolute',
        left: widget.position.x,
        top: widget.position.y,
        width: widget.size.width,
        height: widget.size.height,
        zIndex: widget.zIndex,
        transform: dragState.isDragging ? `translate(${dragTransform.x}px, ${dragTransform.y}px)` : undefined,
        willChange: dragState.isDragging ? 'transform' : undefined,
      }}
      onClick={handleWidgetClick}
      onDoubleClick={handleDoubleClick}
    >
      <WidgetHeader
        widget={widget}
        isSelected={isSelected}
        onStateChange={(state) => onStateChange(widget.id, state)}
        onRename={handleRename}
        onMouseDown={handleMouseDown}
        onClose={() => onClose(widget.id)}
      />

      <WidgetBody widget={widget} />

      {widget.state === 'expanded' && (
        <div className="widget-resize-handles">
          {(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] as ResizeHandle[]).map(
            (handle) => (
              <div
                key={handle}
                className={`resize-handle resize-handle--${handle}`}
                onMouseDown={(e) => handleResizeStart(handle, e)}
              />
            )
          )}
        </div>
      )}
    </div>
  );
};
