import { html, repeat } from '@zuari/dom'
import { createSvgElement } from '@zuari/glyphs/base'
import { ExternalLinkGlyph } from '@zuari/glyphs/icons'
import { state } from '../state'

const copyIcon = createSvgElement('0 0 24 24', '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h2"/>')

function filteredRequests() {
  const q = state.promptFilter.value.trim().toLowerCase()
  const status = state.promptStatusFilter.value
  return state.requests.value.filter(item => {
    if (status !== 'all' && item.status !== status) return false
    if (!q) return true
    return [item.storyKey, item.storyLabel, item.storyFile, item.category, item.dialogueContains]
      .some(v => v.toLowerCase().includes(q))
  })
}

function copyKey(key: string) {
  void navigator.clipboard.writeText(key)
  state.status.value = `Copied request key: ${key}`
}

function requestCard(item: (typeof state.requests.value)[number]) {
  return html`<div class="request-card">
    <div class="request-meta"><strong>${item.storyKey}</strong>
      <div class="request-badges"><span class="usage-label">${item.category} · ${item.status}</span>
        <button class="icon-button small-icon" title="Copy request key" @click=${() => copyKey(item.storyKey)}>${copyIcon}</button></div></div>
    <small>${item.storyLabel} (${item.storyFile}) · ${item.referenceImages.length} ref(s)</small>
    <p>“${item.dialogueContains}”</p>
  </div>`
}

export function generationPage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    <article class="content-panel report-panel">
      <div class="panel-title"><div><h2>Story Requests (${() => filteredRequests().length} of ${() => state.requests.value.length})</h2><p>Tagged story moments ready for artwork generation.</p></div>
        <div class="report-actions">
          <button class="secondary-btn busy-action" @click=${actions.refreshList}>Refresh Prompts</button>
          <button class="icon-button busy-action" aria-label="Copy Markdown" title="Copy Markdown" @click=${actions.copyReport}>${copyIcon}</button>
          <button class="icon-button busy-action" aria-label="Open File" title="Open File" @click=${actions.openReport}>${ExternalLinkGlyph({ size: 18 })}</button>
        </div>
      </div>
      <div class="filter-bar">
        <input id="prompt-filter" class="filter-input" type="search" placeholder="Filter by key, label, category, or dialogue…"
          value=${state.promptFilter} @input=${() => { state.promptFilter.value = (document.getElementById('prompt-filter') as HTMLInputElement | null)?.value || '' }}>
        <div class="filter-pills">
          <button class=${() => state.promptStatusFilter.value === 'all' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.promptStatusFilter.value = 'all' }}>All</button>
          <button class=${() => state.promptStatusFilter.value === 'needs_generation' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.promptStatusFilter.value = 'needs_generation' }}>Needs Art</button>
          <button class=${() => state.promptStatusFilter.value === 'fulfilled' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.promptStatusFilter.value = 'fulfilled' }}>Fulfilled</button>
        </div>
      </div>
      <div class="request-grid">${repeat(filteredRequests, item => item.storyKey, requestCard)}</div>
      <details class="technical-details"><summary>Raw Markdown Prompt Report</summary>
        <pre class="report-box generation-output" aria-live="polite">${state.report}</pre>
      </details>
    </article>
  </section>`
}
