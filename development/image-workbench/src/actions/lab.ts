import * as bridge from '../bridge'
import { showError } from '../errors'
import { state } from '../state'
import { runAction } from './runner'

export function createLabActions() {
  return {
    verifyProject: () => runAction('verify_project'),
    validateStory: () => runAction('story_validate'),
    voiceStatus: () => runAction('voice_status'),
    voiceScan: () => runAction('voice_scan'),
    voiceSynth: () => runAction('voice_synth'),
    voiceMumbles: () => runAction('voice_mumbles'),
    async createDay() {
      if (state.busy.value) return
      const dayEl = document.querySelector<HTMLInputElement>('#lab-day-num')
      const themeEl = document.querySelector<HTMLSelectElement>('#lab-day-theme')
      const seedEl = document.querySelector<HTMLInputElement>('#lab-day-seed')
      const dayNum = Number(dayEl?.value || 11)
      const theme = themeEl?.value || 'campus_hustle'
      const seed = seedEl?.value.trim() ? Number(seedEl.value) : null
      state.busy.value = true
      state.status.value = `Creating Day ${dayNum} (${theme})…`
      try {
        const res = await bridge.createStoryDay(state.projectRoot.value, state.pythonExe.value, dayNum, theme, seed)
        state.output.value = [res.stdout, res.stderr].filter(Boolean).join('\n') || 'Done.'
        state.status.value = res.success ? `Created Day ${dayNum}` : 'Day creation failed'
      } catch (err) { showError(err) }
      finally { state.busy.value = false }
    }
  }
}
