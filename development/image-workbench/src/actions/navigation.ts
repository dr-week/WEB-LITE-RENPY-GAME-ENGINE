import * as bridge from '../bridge'
import { showError } from '../errors'
import { loadProject } from '../project-status'
import { state } from '../state'
import { refreshWorkbenchData, runAction } from './runner'

export function createNavigationActions() {
  return {
    showOverview: () => { state.activeSection.value = 'overview' },
    async refreshOverview() {
      if (await refreshWorkbenchData()) state.activeSection.value = 'overview'
    },
    showImageIntake: () => { state.activeSection.value = 'intake' },
    showGeneration: () => { state.activeSection.value = 'generation' },
    showAudit: () => { state.activeSection.value = 'audit' },
    showImageData: () => { state.activeSection.value = 'data' },
    showStoryLab: () => { state.activeSection.value = 'story' },
    showVoiceLab: () => { state.activeSection.value = 'voice' },
    async refreshList() { state.activeSection.value = 'generation'; await runAction('generate') },
    async audit() { state.activeSection.value = 'audit'; await runAction('audit') },
    async openReport() {
      try { if (await refreshWorkbenchData()) await bridge.openProjectDocument(state.projectRoot.value, 'report') }
      catch (error) { showError(error) }
    },
    async openStoryProposals() {
      try { await bridge.openProjectDocument(state.projectRoot.value, 'story-proposals') }
      catch (error) { showError(error) }
    },
    async copyReport() {
      try {
        if (!await refreshWorkbenchData()) return
        await navigator.clipboard.writeText(state.report.value)
        state.status.value = 'Generation list copied'
      } catch (error) { showError(error) }
    },
    async refreshInventory() {
      try { await loadProject(); state.status.value = 'Inventory refreshed' } catch (error) { showError(error) }
    }
  }
}
