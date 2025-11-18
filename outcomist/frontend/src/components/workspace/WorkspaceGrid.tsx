import { Project } from '../../types';
import { ProjectCard } from '../project/ProjectCard';

interface WorkspaceGridProps {
  projects: Project[];
  viewMode: 'grid' | 'list';
  onProjectDeleted?: () => void;
}

export function WorkspaceGrid({ projects, viewMode, onProjectDeleted }: WorkspaceGridProps) {
  if (viewMode === 'list') {
    // List view - taller cards to ensure previews/files show properly
    return (
      <div className="flex flex-col gap-4 p-6 max-w-[1600px] mx-auto">
        {projects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            className="h-[500px]"
            viewMode="list"
            onDelete={onProjectDeleted}
          />
        ))}
      </div>
    );
  }

  // Grid view - 3x3 grid (stays 3 columns on tablet and up)
  // Taller cards to ensure game previews show properly
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6 max-w-[1920px] mx-auto">
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          project={project}
          className="h-[640px]"
          viewMode="grid"
          onDelete={onProjectDeleted}
        />
      ))}
    </div>
  );
}
