import { Message } from '../../types';
import { useEffect, useRef } from 'react';
import { ProgressIndicator } from './ProgressIndicator';

interface AgentViewProps {
  messages: Message[];
}

export function AgentView({ messages }: AgentViewProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-[#666] text-sm">
        No messages yet. Start a conversation!
      </div>
    );
  }

  return (
    <div className="p-0 overflow-y-auto bg-[#1e1e1e]" style={{ height: '100%' }}>
      {messages.map((message) => (
        <div
          key={message.id}
          className={`py-2.5 px-3.5 my-1 flex flex-col ${
            message.role === 'user' ? 'items-end pr-3.5' : 'items-start pl-3.5'
          }`}
        >
          <div
            className={`py-2 px-3 rounded-lg max-w-[85%] ${
              message.role === 'user'
                ? 'bg-[rgba(59,130,246,0.15)] text-[#e8e8e8]'
                : 'bg-white/[0.03] text-[#d4d4d4]'
            }`}
          >
            <div className="flex items-center gap-1.5 mb-1 text-[10px] text-[#666]">
              <span>
                {new Date(message.timestamp).toLocaleTimeString('en-US', {
                  hour12: false,
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                })}
              </span>
            </div>
            <div className="text-sm leading-relaxed whitespace-pre-wrap break-words">
              {message.content}
            </div>

            {/* Show progress indicator when streaming with progress data */}
            {message.status === 'streaming' && message.progress && (
              <ProgressIndicator progress={message.progress} />
            )}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
