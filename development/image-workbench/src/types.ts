export type PipelineAction =
  | 'generate' | 'preview' | 'apply' | 'audit' | 'reconcile'
  | 'reconcile_apply' | 'catalog' | 'organize' | 'verify_project'
  | 'story_validate' | 'voice_status' | 'voice_scan' | 'voice_synth' | 'voice_mumbles'

export interface ProjectStatus {
  root: string
  rootImages: number
  totalImages: number
  storyImages: number
  unusedImages: number
  categories: ImageCategory[]
  reportText: string
  requests: StoryRequest[]
  storyTargets: StoryTarget[]
}

export interface StoryTarget {
  storyKey: string
  storyFile: string
  storyLabel: string
  dialogueContains: string
  line: number
  currentScene: string
}

export interface StoryRequest {
  storyKey: string
  category: string
  role: string
  storyFile: string
  storyLabel: string
  dialogueContains: string
  referenceImages: string[]
  starterEgg: string
  prompt: string
  imagePath: string
  status: string
}

export interface ImageCategory {
  name: string
  total: number
  storyUsed: number
  unused: number
  files: ImageFile[]
}

export interface ImageFile {
  name: string
  path: string
  usedInStory: boolean
  assetId?: string | null
  storyKey?: string | null
  role?: string | null
  categoryHint?: string | null
  placementStatus: string
  storyTarget?: string | null
}

export interface OperationResult {
  success: boolean
  stdout: string
  stderr: string
}

export interface StageResult {
  copied: string[]
  skipped: string[]
}
