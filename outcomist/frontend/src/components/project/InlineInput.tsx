import { useState, FormEvent, KeyboardEvent } from 'react';

interface InlineInputProps {
  onSend: (message: string) => void;
  onAddFile?: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export function InlineInput({
  onSend,
  onAddFile,
  disabled = false,
  placeholder = 'Type your response...',
}: InlineInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e?: FormEvent) => {
    e?.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="px-3.5 py-3 bg-[rgba(20,20,20,0.8)] border-t border-white/[0.06] flex gap-2.5 items-center">
      {onAddFile && (
        <button
          onClick={onAddFile}
          disabled={disabled}
          className="w-8 h-8 bg-white/5 border border-white/10 rounded-lg text-[#888] text-base flex items-center justify-center cursor-pointer transition-all duration-200 hover:bg-white/[0.08] hover:border-white/[0.15] hover:text-[#aaa] disabled:opacity-50 disabled:cursor-not-allowed"
          title="Add file"
        >
          +
        </button>
      )}
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder={placeholder}
        className="flex-1 bg-[rgba(42,42,42,0.6)] border border-white/10 rounded-[10px] px-3.5 py-2.5 text-[#e8e8e8] text-sm transition-all duration-200 outline-none focus:bg-[rgba(50,50,50,0.8)] focus:border-[rgba(74,144,226,0.4)] focus:shadow-[0_0_0_3px_rgba(74,144,226,0.1)] placeholder:text-[#666]"
      />
      <button
        onClick={() => handleSubmit()}
        disabled={disabled || !message.trim()}
        className="w-8 h-8 bg-[rgba(74,144,226,0.15)] border border-[rgba(74,144,226,0.3)] rounded-lg text-[#4A90E2] text-base flex items-center justify-center cursor-pointer transition-all duration-200 hover:bg-[rgba(74,144,226,0.25)] hover:border-[rgba(74,144,226,0.5)] hover:translate-y-[-1px] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:translate-y-0"
      >
        ↑
      </button>
    </div>
  );
}
