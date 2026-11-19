import { html, repeat } from '@zuari/dom'
import type { ImageCategory, ImageFile, StoryTarget } from '../../types'
import { state } from '../../state'

function eligible(category: ImageCategory) {
  const q = state.placementFilter.value.trim().toLowerCase()
  return category.files.filter(file => !file.usedInStory && file.role !== 'reference'
    && category.name !== 'character_reference'
    && (!q || file.name.toLowerCase().includes(q) || category.name.toLowerCase().includes(q)))
}

const storyTargets = () => state.storyTargets.value
const targetLabel = (t: StoryTarget) => `${t.storyFile.split('/').pop()} · ${t.storyLabel}: ${t.dialogueContains} [line ${t.line}]`

function saveTargetChoice(file: ImageFile, controlId: string) {
  const label = (document.getElementById(controlId) as HTMLInputElement).value
  const target = storyTargets().find(item => targetLabel(item) === label)
  state.placementLabels.value = { ...state.placementLabels.value, [file.path]: label }
  state.placementChoices.value = { ...state.placementChoices.value, [file.path]: target?.storyKey || '' }
}

function clearChoice(file: ImageFile) {
  state.placementLabels.value = { ...state.placementLabels.value, [file.path]: '' }
  state.placementChoices.value = { ...state.placementChoices.value, [file.path]: '' }
}

function pictureRow(file: ImageFile) {
  const controlId = `story-target-${encodeURIComponent(file.path)}`
  return html`<div class="placement-picture"><span><strong>${file.name}</strong>
    <small>${file.path}${file.storyKey ? ' · already assigned' : ''}</small></span>
    <div class="placement-input-row">
      <input id=${controlId} list="story-moment-options" placeholder="Type part of a dialogue…"
        aria-label=${`Choose a story moment for ${file.name}`}
        value=${() => state.placementLabels.value[file.path] || ''}
        @change=${() => saveTargetChoice(file, controlId)}>
      <button class="icon-button small-icon" title="Clear choice" aria-label="Clear choice"
        style=${() => state.placementLabels.value[file.path] ? '' : 'display:none'}
        @click=${() => clearChoice(file)}>×</button>
    </div></div>`
}

export function placementPicker(_actions: ReturnType<typeof import('../../actions').createActions>) {
  const categories = () => state.categories.value.map(category => ({ category, files: eligible(category) }))
    .filter(group => group.files.length)
  const total = () => categories().reduce((sum, group) => sum + group.files.length, 0)
  return html`<section class="work-panel placement-picker">
    <div class="panel-heading"><div><h2>Choose pictures and dialogue locations</h2>
      <p>Open a folder, select a picture, and type words from the dialogue where it should appear.</p></div></div>
    <p>${() => storyTargets().length ? `${storyTargets().length} story moments available.` : 'No story dialogue is available. Refresh Story Prompts first.'}</p>
    <div class="filter-bar" style=${() => storyTargets().length ? '' : 'display:none'}>
      <input id="placement-filter" class="filter-input" type="search" placeholder="Filter unplaced pictures by filename or category…"
        value=${state.placementFilter} @input=${() => { state.placementFilter.value = (document.getElementById('placement-filter') as HTMLInputElement | null)?.value || '' }}>
    </div>
    <details open style=${() => storyTargets().length ? '' : 'display:none'}><summary>Pictures available to place (${total})</summary>
      <datalist id="story-moment-options">${repeat(storyTargets, target => target.storyKey, target => html`
        <option value=${targetLabel(target)}></option>`)}</datalist>
      <div class="placement-list">${repeat(categories, group => group.category.name, group => html`
        <details class="placement-category"><summary>${group.category.name} · ${group.files.length} picture(s)</summary>
          ${repeat(group.files, file => file.path, file => pictureRow(file))}</details>`)}</div>
    </details>
  </section>`
}
