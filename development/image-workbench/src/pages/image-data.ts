import { html, repeat } from '@zuari/dom'
import type { ImageCategory, ImageFile } from '../types'
import { state } from '../state'

function matchesFilter(file: ImageFile) {
  const status = state.catalogStatusFilter.value
  if (status === 'used' && !file.usedInStory) return false
  if (status === 'unused' && file.usedInStory) return false
  const q = state.catalogFilter.value.trim().toLowerCase()
  if (!q) return true
  return [file.name, file.path, file.storyKey || '', file.storyTarget || '', file.assetId || '']
    .some(v => v.toLowerCase().includes(q))
}

function visibleCategories() {
  return state.categories.value
    .map(cat => ({ ...cat, visible: cat.files.filter(matchesFilter) }))
    .filter(cat => cat.visible.length > 0)
}

function coveragePct() {
  const total = Number(state.totalImages.value || 0)
  const used = Number(state.storyImages.value || 0)
  return total ? `${Math.round(used / total * 100)}%` : '0%'
}

function categoryCard(category: ImageCategory & { visible: ImageFile[] }) {
  return html`<details class="category-card" open>
    <summary><span><strong>${category.name}</strong><small>${category.visible.length} of ${category.total} images</small></span>
      <span class="category-counts"><b>${category.storyUsed} used</b><b>${category.unused} unplaced</b></span></summary>
    <ul class="asset-list">${repeat(category.visible, file => file.path, file => html`
      <li class="asset-row"><span class=${file.usedInStory ? 'usage-dot used' : 'usage-dot'}></span>
        <span class="asset-name"><strong>${file.name}</strong><small>${file.role || 'role unset'} · ${file.placementStatus} · ${file.path}</small>
          <small>${file.storyKey ? `Request ${file.storyKey}` : 'No request ID'}${file.assetId ? ` · ${file.assetId}` : ''}${file.storyTarget ? ` · ${file.storyTarget}` : ''}</small></span>
        <span class=${file.usedInStory ? 'usage-label used' : 'usage-label'}>${file.usedInStory ? 'In story' : 'Unplaced'}</span></li>`)}
    </ul>
  </details>`
}

export function imageDataPage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    <div class="compact-summary">
      <span><strong>${state.totalImages}</strong> total assets</span>
      <span><strong>${state.storyImages}</strong> used (${coveragePct})</span>
      <span><strong>${state.unusedImages}</strong> unplaced</span>
      <span><strong>${state.rootImages}</strong> staged</span>
      <button class="secondary-btn busy-action" @click=${actions.rebuildCatalog}>Rebuild Story Catalog</button>
    </div>
    <div class="filter-bar">
      <input id="catalog-filter" class="filter-input" type="search" placeholder="Search assets by filename, request ID, or story target…"
        value=${state.catalogFilter} @input=${() => { state.catalogFilter.value = (document.getElementById('catalog-filter') as HTMLInputElement | null)?.value || '' }}>
      <div class="filter-pills">
        <button class=${() => state.catalogStatusFilter.value === 'all' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.catalogStatusFilter.value = 'all' }}>All</button>
        <button class=${() => state.catalogStatusFilter.value === 'used' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.catalogStatusFilter.value = 'used' }}>In story</button>
        <button class=${() => state.catalogStatusFilter.value === 'unused' ? 'pill-btn active' : 'pill-btn'} @click=${() => { state.catalogStatusFilter.value = 'unused' }}>Unplaced</button>
      </div>
    </div>
    <div class="category-grid" aria-label="Image categories">${repeat(visibleCategories, item => item.name, categoryCard)}</div>
  </section>`
}
