import { useState, useEffect } from 'react';
import { useFiles, useFileContent } from '../../hooks/useFiles';
import type { Project, File } from '../../types';

interface PreviewViewProps {
  project: Project;
}

export function PreviewView({ project }: PreviewViewProps) {
  const { files, loading } = useFiles(project.id);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  useEffect(() => {
    if (files.length > 0 && !selectedFile) {
      const htmlFile = files.find(f => f.name.endsWith('.html'));
      setSelectedFile(htmlFile || files[0]);
    }
  }, [files, selectedFile]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-[#888]">Loading files...</div>
      </div>
    );
  }

  if (files.length === 0) {
    const icons: Record<string, string> = {
      game: '🎮',
      trip: '✈️',
      content: '✍️',
      presentation: '📊',
    };

    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-center p-5">
          <div className="text-6xl mb-4">{icons[project.type] || '📋'}</div>
          <div className="text-lg font-semibold text-[#e0e0e0] mb-2">{project.name}</div>
          <div className="text-sm text-[#888]">No files generated yet</div>
        </div>
      </div>
    );
  }

  if (project.type === 'game' && selectedFile?.name.endsWith('.html')) {
    return <GamePreview file={selectedFile} />;
  }

  return (
    <div className="flex h-full bg-[#1e1e1e]">
      <FileList files={files} selectedFile={selectedFile} onSelect={setSelectedFile} />
      {selectedFile && <FileContent file={selectedFile} />}
    </div>
  );
}

interface GamePreviewProps {
  file: File;
}

function GamePreview({ file }: GamePreviewProps) {
  const { files } = useFiles(file.project_id);
  const { content: htmlContent, loading: htmlLoading } = useFileContent(file.id);
  const [bundledHtml, setBundledHtml] = useState<string>('');

  useEffect(() => {
    const bundleFiles = async () => {
      if (!htmlContent || files.length === 0) return;

      let html = htmlContent;

      // Find and inline CSS files
      const cssFiles = files.filter(f => f.name.endsWith('.css'));
      for (const cssFile of cssFiles) {
        try {
          const response = await fetch(`/api/files/${cssFile.id}/content`);
          const data = await response.json();
          const cssContent = data.content;

          // Replace <link> tag with inline <style>
          html = html.replace(
            new RegExp(`<link[^>]*href=["']${cssFile.name}["'][^>]*>`, 'g'),
            `<style>${cssContent}</style>`
          );
        } catch (e) {
          console.error(`Failed to load ${cssFile.name}:`, e);
        }
      }

      // Find and inline JS files
      const jsFiles = files.filter(f => f.name.endsWith('.js'));
      for (const jsFile of jsFiles) {
        try {
          const response = await fetch(`/api/files/${jsFile.id}/content`);
          const data = await response.json();
          const jsContent = data.content;

          // Replace <script src> with inline <script>
          html = html.replace(
            new RegExp(`<script[^>]*src=["']${jsFile.name}["'][^>]*></script>`, 'g'),
            `<script>${jsContent}</script>`
          );
        } catch (e) {
          console.error(`Failed to load ${jsFile.name}:`, e);
        }
      }

      setBundledHtml(html);
    };

    bundleFiles();
  }, [htmlContent, files, file.id]);

  if (htmlLoading || !htmlContent) {
    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-[#888]">Loading game...</div>
      </div>
    );
  }

  if (!bundledHtml) {
    return (
      <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
        <div className="text-[#888]">Bundling files...</div>
      </div>
    );
  }

  return (
    <div className="w-full h-full overflow-auto bg-white">
      <iframe
        srcDoc={bundledHtml}
        className="w-full min-h-full border-0"
        title="Game Preview"
        sandbox="allow-scripts"
        style={{ height: '100%' }}
      />
    </div>
  );
}

interface FileListProps {
  files: File[];
  selectedFile: File | null;
  onSelect: (file: File) => void;
}

function FileList({ files, selectedFile, onSelect }: FileListProps) {
  return (
    <div className="w-48 border-r border-[#333] bg-[#1a1a1a] overflow-y-auto">
      <div className="p-3 text-xs text-[#888] font-semibold">FILES</div>
      {files.map(file => (
        <button
          key={file.id}
          onClick={() => onSelect(file)}
          className={`w-full text-left px-3 py-2 text-sm hover:bg-[#2a2a2a] transition-colors ${
            selectedFile?.id === file.id ? 'bg-[#2a2a2a] text-[#569cd6]' : 'text-[#ccc]'
          }`}
        >
          <div className="flex items-center gap-2">
            <span className="flex-shrink-0">{getFileIcon(file.name)}</span>
            <span className="truncate">{file.name}</span>
          </div>
        </button>
      ))}
    </div>
  );
}

interface FileContentProps {
  file: File;
}

function FileContent({ file }: FileContentProps) {
  const { content, loading } = useFileContent(file.id);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-[#888]">Loading...</div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-[#888]">Failed to load file</div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[#ccc] text-sm">{file.name}</span>
          <button
            onClick={() => downloadFile(file, content)}
            className="px-3 py-1 text-xs bg-[#007acc] hover:bg-[#005a9e] text-white rounded transition-colors"
          >
            Download
          </button>
        </div>
        <pre className="bg-[#0d0d0d] rounded p-4 overflow-x-auto">
          <code className="text-[#d4d4d4] text-sm font-mono whitespace-pre">{content}</code>
        </pre>
      </div>
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

function downloadFile(file: File, content: string): void {
  const blob = new Blob([content], { type: file.mime_type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = file.name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
