import { html } from '@zuari/dom'
import { state } from '../state'
import { auditSummary } from './audit/summary'
import { placementPicker } from './audit/placement-picker'

export function auditPage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    <article class="content-panel"><div class="panel-title"><div><h2>1. Script & Asset Check</h2><p>Verify that every story background and CG points to an existing file.</p></div>
      <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.audit}>Check Script References</button></div>
      <p class="audit-summary" aria-live="polite">${() => auditSummary(state.output.value)}</p>
      <details class="technical-details"><summary>Scan Details</summary>
        <pre class="output-box audit-output">${state.output}</pre>
      </details>
    </article>
    <section class="work-panel reconcile-panel">
      <div class="panel-heading"><div><h2>2. Place Unused Art in Story</h2><p>Bind unused images to unillustrated lines below, then preview or apply.</p></div></div>
      <div class="quick-actions">
        <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.placePicturesInStory}>Add Chosen & Matched Pictures (${() => Object.values(state.placementChoices.value).filter(Boolean).length} chosen)</button>
        <button class="secondary-btn busy-action" @click=${actions.reconcile}>Preview Matches</button>
        <button class="secondary-btn busy-action" @click=${actions.rebuildCatalog}>Rebuild Story Catalog</button>
      </div>
      ${placementPicker(actions)}
    </section>
  </section>`
}
