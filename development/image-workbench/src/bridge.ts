import { invoke } from '@tauri-apps/api/core'
import { open } from '@tauri-apps/plugin-dialog'
import type { OperationResult, PipelineAction, ProjectStatus, StageResult } from './types'
import { browserPreview } from './preview/mode'
import { fixtureResult, fixtureStatus, pickFixtureImages, stageFixture } from './preview/fixture'

export async function defaultProjectRoot(): Promise<string> {
  if (browserPreview) return 'Browser preview · sample project'
  return invoke('default_project_root')
}

export async function projectStatus(projectRoot: string): Promise<ProjectStatus> {
  if (browserPreview) return fixtureStatus()
  return invoke('project_status', { projectRoot })
}

export async function selectImages(): Promise<string[]> {
  if (browserPreview) return pickFixtureImages()
  const files = await open({ multiple: true, filters: [{ name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'webp'] }] })
  return Array.isArray(files) ? files : files ? [files] : []
}

export async function selectProjectFolder(): Promise<string | null> {
  if (browserPreview) return 'Browser preview · sample project'
  const result = await open({ directory: true, multiple: false })
  return typeof result === 'string' ? result : null
}

export async function stageImages(projectRoot: string, files: string[]): Promise<StageResult> {
  if (browserPreview) return stageFixture(files)
  return invoke('stage_images', { projectRoot, files })
}

export async function prepareImageMetadata(projectRoot: string, imageName: string, storyKey: string | null, category: string, role: string): Promise<string> {
  if (browserPreview) return `Prepared ${imageName} for ${storyKey || 'category-only review'}`
  return invoke('prepare_image_metadata', { projectRoot, imageName, storyKey, category, role })
}

export async function assignAssetToStory(projectRoot: string, imagePath: string, storyKey: string): Promise<string> {
  if (browserPreview) return `${imagePath} assigned to ${storyKey}`
  return invoke('assign_asset_to_story', { projectRoot, imagePath, storyKey })
}

export async function runScript(projectRoot: string, pythonExe: string, action: PipelineAction): Promise<OperationResult> {
  if (browserPreview) return fixtureResult(action)
  return invoke('run_project_script', { projectRoot, pythonExe, action })
}

export async function createStoryDay(projectRoot: string, pythonExe: string, dayNum: number, theme: string, seed: number | null): Promise<OperationResult> {
  if (browserPreview) return { success: true, stdout: `Preview: Created Day ${dayNum} (${theme})`, stderr: '' }
  return invoke('create_story_day', { projectRoot, pythonExe, dayNum, theme, seed })
}

export async function openProjectDocument(projectRoot: string, document: string): Promise<void> {
  if (browserPreview) return
  return invoke('open_project_document', { projectRoot, document })
}
