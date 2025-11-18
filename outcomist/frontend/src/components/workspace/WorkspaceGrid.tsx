import { Project } from '../../types';
import { ProjectCard } from '../project/ProjectCard';

interface WorkspaceGridProps {
  projects: Project[];
}

export function WorkspaceGrid({ projects }: WorkspaceGridProps) {
  return (
    <div className="grid grid-cols-2 gap-6 p-6 max-w-[1600px] mx-auto">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}
