/**
 * Extract task plan from AI's initial response
 */

export interface ExtractedTask {
  label: string;
  order: number;
}

/**
 * Extract tasks from AI response text
 * Looks for numbered lists, bullet lists, or "I'll/I will" statements
 */
export function extractTasksFromPlan(text: string): ExtractedTask[] {
  const tasks: ExtractedTask[] = [];

  // Try numbered lists first (1. Task, 2. Task)
  const numberedMatches = text.match(/^\s*\d+\.\s+(.+)$/gm);
  if (numberedMatches && numberedMatches.length >= 2) {
    numberedMatches.forEach((match, index) => {
      const label = match.replace(/^\s*\d+\.\s+/, '').trim();
      if (label.length > 0 && label.length < 100) {
        tasks.push({ label, order: index });
      }
    });
    return tasks;
  }

  // Try bullet lists (-, *, •)
  const bulletMatches = text.match(/^\s*[-*•]\s+(.+)$/gm);
  if (bulletMatches && bulletMatches.length >= 2) {
    bulletMatches.slice(0, 6).forEach((match, index) => {
      const label = match.replace(/^\s*[-*•]\s+/, '').trim();
      if (label.length > 0 && label.length < 100) {
        tasks.push({ label, order: index });
      }
    });
    return tasks;
  }

  // Try "I'll" or "I will" statements
  const willMatches = text.match(/(?:I'll|I will)\s+([^.!?]+)/gi);
  if (willMatches && willMatches.length >= 2) {
    willMatches.slice(0, 6).forEach((match, index) => {
      const label = match.replace(/^(?:I'll|I will)\s+/i, '').trim();
      if (label.length > 0 && label.length < 100) {
        tasks.push({ label, order: index });
      }
    });
    return tasks;
  }

  // No clear plan found - return empty (will use generic tasks)
  return [];
}
