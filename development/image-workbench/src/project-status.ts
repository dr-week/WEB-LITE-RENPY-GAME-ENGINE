import { projectStatus, runScript } from './bridge'
import { state } from './state'

export async function loadProject(refreshList = true): Promise<void> {
  let reportError = ''
  if (refreshList) {
    const result = await runScript(state.projectRoot.value, state.pythonExe.value, 'generate')
    if (!result.success) reportError = result.stderr || result.stdout || 'Generation list refresh failed.'
  }
  const current = await projectStatus(state.projectRoot.value)
  state.projectRoot.value = current.root
  state.rootImages.value = String(current.rootImages)
  state.totalImages.value = String(current.totalImages)
  state.storyImages.value = String(current.storyImages)
  state.unusedImages.value = String(current.unusedImages)
  state.categories.value = current.categories
  state.rootFiles.value = current.categories.flatMap(category =>
    category.name === 'Uncategorized' ? category.files : [])
  state.requests.value = current.requests
  state.storyTargets.value = current.storyTargets
  state.report.value = reportError
    ? `Could not refresh the generation list. The displayed report may be old.\n\n${reportError}`
    : current.reportText
}
