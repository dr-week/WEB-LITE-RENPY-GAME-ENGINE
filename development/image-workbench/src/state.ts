import { signal } from '@zuari/signals'
import { initialSection } from './preview/mode'

export const state = {
  projectRoot: signal('Finding game project…'),
  pythonExe: signal(localStorage.getItem('lola-python') || 'python'),
  rootImages: signal('0'),
  totalImages: signal('—'),
  storyImages: signal('—'),
  unusedImages: signal('—'),
  categories: signal([] as import('./types').ImageCategory[]),
  rootFiles: signal([] as import('./types').ImageFile[]),
  requests: signal([] as import('./types').StoryRequest[]),
  storyTargets: signal([] as import('./types').StoryTarget[]),
  stagedAssignments: signal({} as Record<string, { storyKey: string, category: string, role: string }>),
  placementChoices: signal({} as Record<string, string>),
  placementLabels: signal({} as Record<string, string>),
  promptFilter: signal(''),
  promptStatusFilter: signal<'all' | 'needs_generation' | 'fulfilled'>('all'),
  catalogFilter: signal(''),
  catalogStatusFilter: signal<'all' | 'used' | 'unused'>('all'),
  placementFilter: signal(''),
  report: signal('Refreshing the current story and image inventory…'),
  output: signal('Ready. Add images, preview the plan, then apply it.'),
  status: signal('Connecting to project…'),
  activeSection: signal(initialSection),
  busy: signal(false),
  canApply: signal(false),
  canReconcileApply: signal(false)
}
