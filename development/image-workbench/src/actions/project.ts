import * as bridge from '../bridge'
import { showError } from '../errors'
import { loadProject } from '../project-status'
import { state } from '../state'
import { browserPreview } from '../preview/mode'

export function createProjectActions() {
  return {
    showError,
    async boot() {
      try {
        state.projectRoot.value = browserPreview
          ? await bridge.defaultProjectRoot()
          : localStorage.getItem('lola-project-root') || await bridge.defaultProjectRoot()
        await loadProject()
        state.status.value = 'Project ready'
      } catch (error) { showError(error) }
    },
    async chooseProject() {
      if (state.busy.value) { state.status.value = 'Wait for the current operation to finish'; return }
      try {
        const folder = await bridge.selectProjectFolder()
        if (!folder) return
        state.projectRoot.value = folder
        localStorage.setItem('lola-project-root', folder)
        await loadProject()
        state.status.value = 'Project folder changed'
      } catch (error) { showError(error) }
    },
    setPython() {
      const input = document.querySelector<HTMLInputElement>('#python-exe')
      if (!input) return
      state.pythonExe.value = input.value.trim() || 'python'
      localStorage.setItem('lola-python', state.pythonExe.value)
    },
    async openGuide() {
      try { await bridge.openProjectDocument(state.projectRoot.value, 'guide') }
      catch (error) { showError(error) }
    },
    async openTemplate() {
      try { await bridge.openProjectDocument(state.projectRoot.value, 'template') }
      catch (error) { showError(error) }
    },
    async openStoryBible() {
      try { await bridge.openProjectDocument(state.projectRoot.value, 'story-bible') }
      catch (error) { showError(error) }
    },
    async openRoadmap() {
      try { await bridge.openProjectDocument(state.projectRoot.value, 'roadmap') }
      catch (error) { showError(error) }
    }
  }
}
