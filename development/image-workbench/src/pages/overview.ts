import { html, repeat } from '@zuari/dom'
import { state } from '../state'

function counts() {
  const files = state.categories.value.flatMap(category => category.files)
  const needsReview = files.filter(file => ['needs_review', 'generated', 'untracked', 'staged'].includes(file.placementStatus)).length
  const references = files.filter(file => file.role === 'reference').length
  const requests = state.requests.value.filter(request => request.status === 'needs_generation').length
  return { needsReview, references, requests }
}

function categoryBar(category: (typeof state.categories.value)[number], max: number) {
  const totalW = max ? Math.max(4, category.total / max * 100) : 0
  const usedW = category.total ? Math.round(category.storyUsed / category.total * 100) : 0
  return html`<div class="overview-category"><span>${category.name}</span>
    <div class="mini-bar" title=${`${category.storyUsed} used of ${category.total}`}><i style=${`width:${totalW}%`}><em style=${`width:${usedW}%`}></em></i></div>
    <b>${category.storyUsed}/${category.total}</b></div>`
}

export function overviewPage(actions: ReturnType<typeof import('../actions').createActions>) {
  const summary = () => counts()
  const max = () => Math.max(1, ...state.categories.value.map(category => category.total))
  return html`<section class="page-stack">
    <div class="stats overview-stats">
      <button class="stat-card stat-link" @click=${actions.showImageData}><span>Total Assets</span><strong>${state.totalImages}</strong><small>all categories & intake</small></button>
      <button class="stat-card stat-link" @click=${actions.showImageData}><span>Used in Story</span><strong>${state.storyImages}</strong><small>referenced by story scripts</small></button>
      <button class="stat-card stat-link" @click=${actions.showAudit}><span>Needs Review</span><strong>${() => summary().needsReview}</strong><small>awaiting story placement</small></button>
      <button class="stat-card stat-link" @click=${actions.showGeneration}><span>Open Prompts</span><strong>${() => summary().requests}</strong><small>unillustrated story beats</small></button>
    </div>
    <div class="overview-grid">
      <article class="content-panel"><div class="panel-title"><div><h2>Pipeline Stages & Maintenance</h2><p>${() => state.storyTargets.value.length} unillustrated story lines available</p></div></div>
        <div class="pipeline-stage"><b>01</b><span><strong>${state.rootImages}</strong><small>Staged in intake · waiting for preview</small></span></div>
        <div class="pipeline-stage"><b>02</b><span><strong>${() => Math.max(0, Number(state.totalImages.value || 0) - Number(state.rootImages.value || 0))}</strong><small>Organized in category folders</small></span></div>
        <div class="pipeline-stage"><b>03</b><span><strong>${state.storyImages}</strong><small>Placed and referenced by story scripts</small></span></div>
        <p class="overview-note">${() => summary().references} reference-only files · filename hints never auto-select dialogue.</p>
        <div class="quick-actions">
          <button class="secondary-btn busy-action" @click=${actions.refreshOverview}>Refresh All</button>
          <button class="secondary-btn busy-action" @click=${actions.rebuildCatalog}>Rebuild Story Catalog</button>
          <button class="secondary-btn busy-action" @click=${actions.organizeLoose}>Organize Loose Art</button>
        </div>
      </article>
      <article class="content-panel"><div class="panel-title"><div><h2>Assets by Category</h2><p>Story-used vs. total per folder</p></div></div>
        <div class="overview-bars">${repeat(state.categories, item => item.name, item => categoryBar(item, max()))}</div>
      </article>
    </div>
  </section>`
}
