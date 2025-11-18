import { useState, useEffect } from 'react';
import { Toolbar } from './components/workspace/Toolbar';
import { WorkspaceGrid } from './components/workspace/WorkspaceGrid';
import { NewProjectModal } from './components/workspace/NewProjectModal';
import { OnboardingFlow } from './components/onboarding/OnboardingFlow';
import { useProjects } from './hooks/useProjects';
import { api } from './api/client';
import type { ProjectType } from './types';

type AppView = 'onboarding' | 'workspace';

export default function App() {
  const { projects, loading, refetch } = useProjects();
  const [currentView, setCurrentView] = useState<AppView>('workspace');
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  // Skip onboarding - always show workspace
  // useEffect(() => {
  //   if (!loading && projects.length === 0) {
  //     setCurrentView('onboarding');
  //   }
  // }, [loading, projects.length]);

  const handleCreateProject = async (data?: {
    type: ProjectType;
    name: string;
    description: string;
  }) => {
    if (isCreatingProject) return;

    setIsCreatingProject(true);
    setShowNewProjectModal(false);

    try {
      // Create project with auto-generated name
      const projectCount = projects.length + 1;
      const project = await api.createProject({
        name: data?.name || `Project ${projectCount}`,
        description: data?.description || undefined,
        type: data?.type || 'game',
      });

      await api.createSession(project.id, 'Main Session');
      await refetch();
      setCurrentView('workspace');
    } catch (error) {
      console.error('Failed to create project:', error);
      alert('Failed to create project');
    } finally {
      setIsCreatingProject(false);
    }
  };

  const handleQuickCreate = () => {
    handleCreateProject();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1e1e1e] flex items-center justify-center">
        <div className="text-[#aaa]">Loading workspace...</div>
      </div>
    );
  }

  if (currentView === 'onboarding') {
    return (
      <OnboardingFlow
        onComplete={handleCreateProject}
        onSkip={() => setCurrentView('workspace')}
      />
    );
  }

  return (
    <div className="min-h-screen">
      <Toolbar onNewProject={handleQuickCreate} />
      <WorkspaceGrid projects={projects} />
    </div>
  );
}
