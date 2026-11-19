import type { OperationResult, PipelineAction, ProjectStatus, StageResult } from '../types'

let waiting = 2
let placed = 1
let stagedNames = ['new_campus_scene.jpg', 'new_background.jpg']
const report = `# Fresh story image requirements\n\n### Morning arrival\n- Story target: 40_story/prologue/day.rpy:24\n- Dialogue: Maya pauses at the busy campus entrance.\n- References: images/character_reference/maya_turnaround.png\n- Prompt: [SCENE: campus arrival] [BEAT: hesitant pause] [STYLE: illustrated cast, photo-real setting] [STARTER_EGG: distracted-glance gag]\n`

export const fixtureStatus = (): ProjectStatus => ({
  root: 'Browser preview · sample project', rootImages: waiting, totalImages: 12 + waiting,
  storyImages: placed, unusedImages: 12 + waiting - placed,
  categories: [{ name: 'campus', total: 4, storyUsed: 1, unused: 3, files: [
    { name: 'main_gate.jpg', path: 'images/campus/main_gate.jpg', usedInStory: true, assetId: 'asset_a102', storyKey: 'story_01a102', role: 'cg', categoryHint: 'campus', placementStatus: 'placed', storyTarget: 'day_01_college.rpy · arrive_college' },
    { name: 'quiet_hallway.jpg', path: 'images/campus/quiet_hallway.jpg', usedInStory: false, role: 'cg', placementStatus: 'needs_review' },
    { name: 'courtyard_rain.jpg', path: 'images/campus/courtyard_rain.jpg', usedInStory: false, role: 'cg', placementStatus: 'needs_review' },
    { name: 'library_evening.jpg', path: 'images/campus/library_evening.jpg', usedInStory: false, role: 'background', placementStatus: 'organized' }
  ] }, { name: 'character_reference', total: 8, storyUsed: 0, unused: 8, files: [
    ...['turnaround_front.png', 'turnaround_side.png', 'blue_outfit_front.png', 'blue_outfit_back.png',
      'blue_outfit_pose_1.png', 'blue_outfit_pose_2.png', 'expression_sheet.png', 'casual_pose.png']
      .map(name => ({ name, path: `images/character_reference/${name}`, usedInStory: false, role: 'reference', placementStatus: 'reference_only' }))
  ] }, { name: 'Uncategorized', total: waiting, storyUsed: 0, unused: waiting, files: stagedNames.map((name, index) => ({
    name, path: name, usedInStory: false, role: 'cg', categoryHint: 'campus', placementStatus: 'staged', storyKey: index === 0 ? 'story_01a102' : ''
  })) }],
  requests: [{ storyKey: 'story_01a102', category: 'campus', role: 'cg',
    storyFile: '40_story/prologue/day_01_college.rpy', storyLabel: 'arrive_college',
    dialogueContains: 'Maya pauses at the busy campus entrance.', referenceImages: [],
    starterEgg: 'distracted-glance gag', prompt: 'Campus arrival scene', imagePath: '', status: 'needs_generation' }],
  storyTargets: [{ storyKey: 'story_01a102', storyFile: '40_story/prologue/day_01_college.rpy',
    storyLabel: 'arrive_college', dialogueContains: 'Maya pauses at the busy campus entrance.', line: 24, currentScene: 'bg_campus' }],
  reportText: report
})

export function fixtureResult(action: PipelineAction): OperationResult {
  if (action === 'apply') { waiting = 0; stagedNames = [] }
  if (action === 'reconcile_apply') placed += 1
  const stdout = action === 'reconcile' ? 'PLACE cg_courtyard_rain → day_01_campus at line 24' : `Browser preview: ${action} completed using sample data.`
  return { success: true, stdout, stderr: '' }
}

export function stageFixture(files: string[]): StageResult {
  stagedNames.push(...files.map(file => file.split(/[\\/]/).pop() || file))
  waiting = stagedNames.length
  return { copied: files, skipped: [] }
}

export function pickFixtureImages(): string[] { return ['browser_preview_scene.jpg'] }
