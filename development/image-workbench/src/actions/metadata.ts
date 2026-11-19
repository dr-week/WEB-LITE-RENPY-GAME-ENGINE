import * as bridge from '../bridge'
import { showError } from '../errors'
import { loadProject } from '../project-status'
import { state } from '../state'

export async function assignStagedImage(path: string, storyKey: string, category: string, role: string) {
  if (state.busy.value) return
  state.busy.value = true
  try {
    state.output.value = await bridge.prepareImageMetadata(
      state.projectRoot.value, path, storyKey || null, category, role)
    await loadProject()
    state.status.value = 'Image metadata saved; preview the intake plan'
  } catch (error) { showError(error) }
  finally { state.busy.value = false }
}
