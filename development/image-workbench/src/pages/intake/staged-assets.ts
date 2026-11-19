import { html, repeat } from '@zuari/dom'
import type { ImageFile } from '../../types'
import { state } from '../../state'

const categories = ['college', 'food_drink', 'general_scenes', 'hobbies_outdoors',
  'home_lodging', 'public_places', 'relationships', 'shops_markets', 'social_events', 'transport']
const roles = ['cg', 'background', 'reference']
const controlId = (file: ImageFile, field: string) => `${field}-${encodeURIComponent(file.path)}`

function assignment(file: ImageFile) {
  return state.stagedAssignments.value[file.path] || {
    storyKey: file.storyKey || '', category: file.categoryHint || 'general_scenes',
    role: file.role || 'cg'
  }
}

function requestSummary(file: ImageFile) {
  const request = state.requests.value.find(item => item.storyKey === assignment(file).storyKey)
  return request
    ? `${request.storyFile} · ${request.storyLabel} · “${request.dialogueContains}” · ${request.referenceImages.length} references`
    : 'No story insertion selected; this file will only be categorized.'
}

function setField(file: ImageFile, field: 'storyKey' | 'category' | 'role', value: string) {
  const next = { ...assignment(file), [field]: value }
  if (field === 'storyKey') {
    const request = state.requests.value.find(item => item.storyKey === value)
    if (request) { next.category = request.category; next.role = request.role }
  }
  if (field === 'role' && value === 'reference') next.storyKey = ''
  state.stagedAssignments.value = { ...state.stagedAssignments.value, [file.path]: next }
}

function stagedFile(file: ImageFile, actions: ReturnType<typeof import('../../actions').createActions>) {
  return html`<article class="staged-asset-card"><div class="staged-file-title"><strong>${file.name}</strong>
    <small>${file.assetId || 'Asset ID assigned on import'} · ${file.placementStatus}</small></div>
    <label>Story request<select id=${controlId(file, 'request')} value=${() => assignment(file).storyKey}
      @change=${() => setField(file, 'storyKey', selectControlValue(file, 'request'))}>
      <option value="">Category only · review later</option>
      ${repeat(state.requests, item => item.storyKey, item => html`<option value=${item.storyKey}>${item.storyKey} · ${item.storyLabel} · ${item.status}</option>`)}</select></label>
    <small class="staged-target">${() => requestSummary(file)}</small>
    <label>Category<select id=${controlId(file, 'category')} value=${() => assignment(file).category}
      @change=${() => setField(file, 'category', selectControlValue(file, 'category'))}>
      ${repeat([...new Set([...categories, ...state.categories.value.map(item => item.name), ...state.requests.value.map(item => item.category)])].sort(), item => item, item => html`<option value=${item}>${item}</option>`)}</select></label>
    <label>Role<select id=${controlId(file, 'role')} value=${() => assignment(file).role}
      @change=${() => setField(file, 'role', selectControlValue(file, 'role'))}>
      ${repeat(roles, item => item, item => html`<option value=${item}>${item}</option>`)}</select></label>
    <button class="secondary-btn busy-action" @click=${() => { const value = assignment(file); return actions.assignImage(file.path, value.storyKey, value.category, value.role) }}>Save routing</button>
  </article>`
}

function selectControlValue(file: ImageFile, field: string) {
  return (document.getElementById(controlId(file, field)) as HTMLSelectElement | null)?.value || ''
}

export function stagedAssets(actions: ReturnType<typeof import('../../actions').createActions>) {
  return html`<section class="content-panel staged-assets"><div class="panel-title"><div><h2>Route staged images</h2>
    <p>Choose the request, category, and role. The request ID must match its exact dialogue anchor.</p></div></div>
    <div class="empty-state" style=${() => Number(state.rootImages.value) ? 'display:none' : ''}>No staged images in <code>game/images</code> root. Select or drop image files above to begin.</div>
    <div class="staged-asset-list">${repeat(state.rootFiles, file => file.path, file => stagedFile(file, actions))}</div>
  </section>`
}
