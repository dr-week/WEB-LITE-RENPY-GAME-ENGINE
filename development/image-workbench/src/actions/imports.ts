import { runAction } from './runner'
import { chooseImages, dropImages } from '../image-actions'
import { state } from '../state'
import { reconcileConfirmation } from './reconcile-confirmation'
import * as bridge from '../bridge'
import { showError } from '../errors'

export function createImportActions() {
  return {
    chooseImages,
    dropFiles: dropImages,
    preview: () => runAction('preview'),
    apply: () => {
      if (state.canApply.value && window.confirm('Apply the reviewed plan? Exact request IDs will be placed at their story targets. Images without a verified target will only be categorized for review.')) return runAction('apply')
    },
    reconcile: () => runAction('reconcile'),
    async placePicturesInStory() {
      const choices = Object.entries(state.placementChoices.value).filter(([, key]) => key)
      if (new Set(choices.map(([, key]) => key)).size !== choices.length) {
        state.status.value = 'Choose a different story moment for each picture'; return
      }
      if (choices.length) {
        if (state.busy.value) return
        state.busy.value = true
        try {
          for (const [imagePath, storyKey] of choices) {
            await bridge.assignAssetToStory(state.projectRoot.value, imagePath, storyKey)
          }
          state.status.value = `Checking ${choices.length} chosen picture(s)…`
        } catch (error) { showError(error); return }
        finally { state.busy.value = false }
      }
      await runAction('reconcile')
      if (!state.canReconcileApply.value) {
        if (!choices.length) state.status.value = 'No clear story matches yet. Choose a dialogue for pictures below.'
        return
      }
      if (window.confirm(reconcileConfirmation(state.output.value))) {
        await runAction('reconcile_apply')
        if (state.status.value === 'Workflow complete') state.placementChoices.value = {}
      } else {
        state.status.value = 'No pictures were added. Your scene choices are saved.'
      }
    },
    reconcileApply: () => state.canReconcileApply.value &&
      window.confirm(reconcileConfirmation(state.output.value)) && runAction('reconcile_apply'),
    rebuildCatalog: () => runAction('catalog'),
    organizeLoose: () => runAction('organize')
  }
}
