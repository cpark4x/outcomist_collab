import { useFiles } from '../../hooks/useFiles';

interface FilesViewProps {
  projectId: string;
}

export function FilesView({ projectId }: FilesViewProps) {
  const { files, loading } = useFiles(projectId);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-[#888]">Loading files...</div>
      </div>
    );
  }

  if (files.length === 0) {
    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-center p-5">
          <div className="text-4xl mb-3">📁</div>
          <div className="text-[#888] text-sm">No files yet</div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-[#1e1e1e] p-4 font-mono text-sm overflow-y-auto">
      <div className="text-xs text-[#888] mb-4 font-semibold">PROJECT FILES</div>
      {files.map(file => (
        <div key={file.id} className="flex items-center gap-3 py-2 px-3 hover:bg-[#2a2a2a] rounded transition-colors">
          <span className="text-lg">{getFileIcon(file.name)}</span>
          <span className="flex-1 text-[#ccc] truncate">{file.name}</span>
          <span className="text-xs text-[#888]">{formatBytes(file.size)}</span>
        </div>
      ))}
    </div>
  );
}

function getFileIcon(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase();
  const icons: Record<string, string> = {
    html: '📄',
    css: '🎨',
    js: '⚡',
    json: '📋',
    md: '📝',
    txt: '📄',
  };
  return icons[ext || ''] || '📄';
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 10) / 10 + ' ' + sizes[i];
}
