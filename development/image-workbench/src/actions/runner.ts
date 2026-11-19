import * as bridge from '../bridge'
import { showError } from '../errors'
import { loadProject } from '../project-status'
import { state } from '../state'
import type { PipelineAction } from '../types'

export async function refreshWorkbenchData(): Promise<boolean> {
  if (state.busy.value) return false
  state.busy.value = true
  try {
    await loadProject()
    return !state.report.value.startsWith('Could not refresh the generation list.')
  } catch (error) { showError(error); return false }
  finally { state.busy.value = false }
}

export async function runAction(action: PipelineAction): Promise<void> {
  if (state.busy.value) { state.status.value = 'Wait for the current operation to finish'; return }
  state.busy.value = true
  state.canApply.value = false
  state.canReconcileApply.value = false
  state.status.value = `Running ${action}…`
  try {
    const result = await bridge.runScript(state.projectRoot.value, state.pythonExe.value, action)
    state.output.value = [result.stdout, result.stderr].filter(Boolean).join('\n') || 'Script completed without output.'
    state.status.value = result.success ? 'Workflow complete' : 'Script failed'
    await loadProject(action !== 'generate')
    if (action === 'generate' && !result.success) state.report.value = `Could not refresh the generation list.\n\n${result.stderr || result.stdout || 'Generation list refresh failed.'}`
    state.canApply.value = action === 'preview' && result.success && Number(state.rootImages.value) > 0
    state.canReconcileApply.value = action === 'reconcile' && result.success && /PLACE /.test(result.stdout)
  } catch (error) { showError(error) }
  finally { state.busy.value = false }
}
