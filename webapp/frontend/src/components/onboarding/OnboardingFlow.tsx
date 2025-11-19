import { useState } from 'react';
import { WelcomeScreen } from './WelcomeScreen';
import { FeaturesScreen } from './FeaturesScreen';
import { ProjectTypeScreen } from './ProjectTypeScreen';
import { ProjectDetailsScreen } from './ProjectDetailsScreen';
import { SuccessScreen } from './SuccessScreen';
import type { ProjectType } from '../../types';

export type OnboardingStep = 'welcome' | 'features' | 'type' | 'details' | 'success';

interface OnboardingData {
  projectType: ProjectType | null;
  projectName: string;
  projectDescription: string;
}

interface OnboardingFlowProps {
  onComplete: (data: { type: ProjectType; name: string; description: string }) => void;
  onSkip?: () => void;
}

export function OnboardingFlow({ onComplete, onSkip }: OnboardingFlowProps) {
  const [step, setStep] = useState<OnboardingStep>('welcome');
  const [data, setData] = useState<OnboardingData>({
    projectType: null,
    projectName: '',
    projectDescription: '',
  });

  const handleNext = () => {
    const steps: OnboardingStep[] = ['welcome', 'features', 'type', 'details', 'success'];
    const currentIndex = steps.indexOf(step);
    if (currentIndex < steps.length - 1) {
      setStep(steps[currentIndex + 1]);
    }
  };

  const handleBack = () => {
    const steps: OnboardingStep[] = ['welcome', 'features', 'type', 'details', 'success'];
    const currentIndex = steps.indexOf(step);
    if (currentIndex > 0) {
      setStep(steps[currentIndex - 1]);
    }
  };

  const handleSelectType = (type: ProjectType) => {
    setData({ ...data, projectType: type });
    setStep('details');
  };

  const handleSubmitDetails = (name: string, description: string) => {
    setData({ ...data, projectName: name, projectDescription: description });
    setStep('success');
  };

  const handleFinish = () => {
    if (data.projectType && data.projectName) {
      onComplete({
        type: data.projectType,
        name: data.projectName,
        description: data.projectDescription,
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#1e1e1e] flex items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        {step === 'welcome' && <WelcomeScreen onNext={handleNext} onSkip={onSkip} />}
        {step === 'features' && <FeaturesScreen onNext={handleNext} onBack={handleBack} />}
        {step === 'type' && (
          <ProjectTypeScreen
            onSelectType={handleSelectType}
            onBack={handleBack}
            onSkip={onSkip}
          />
        )}
        {step === 'details' && data.projectType && (
          <ProjectDetailsScreen
            projectType={data.projectType}
            onSubmit={handleSubmitDetails}
            onBack={handleBack}
          />
        )}
        {step === 'success' && <SuccessScreen onFinish={handleFinish} />}
      </div>
    </div>
  );
}
