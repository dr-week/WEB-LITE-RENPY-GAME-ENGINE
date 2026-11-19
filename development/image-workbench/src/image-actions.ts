import * as bridge from './bridge'
import { showError } from './errors'
import { loadProject } from './project-status'
import { state } from './state'

async function stageFiles(files: string[]): Promise<void> {
  if (!files.length) return
  if (state.busy.value) {
    state.status.value = 'Wait for the current operation to finish before adding files'
    return
  }
  state.busy.value = true
  state.canApply.value = false
  try {
    const result = await bridge.stageImages(state.projectRoot.value, files)
    state.output.value = `Added ${result.copied.length} image(s).\n${result.copied.join('\n')}\n${result.skipped.join('\n')}`
    state.status.value = result.skipped.length ? 'Some files were skipped' : 'Images ready to preview'
    await loadProject()
  } catch (error) { showError(error) }
  finally { state.busy.value = false }
}

export async function chooseImages(): Promise<void> {
  try { await stageFiles(await bridge.selectImages()) }
  catch (error) { showError(error) }
}

export const dropImages = stageFiles
