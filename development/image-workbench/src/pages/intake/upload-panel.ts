import { html } from '@zuari/dom'
import { PlusGlyph } from '@zuari/glyphs/icons'

export function uploadPanel(actions: ReturnType<typeof import('../../actions').createActions>) {
  return html`<section class="work-panel zuari-surface-liquid" data-zuari-tint="rose">
    <div class="panel-heading"><div><h2>Select or drop images anywhere</h2>
      <p>Drag & drop PNG, JPG, or WebP files into this window to stage them in <code>game/images</code>.</p></div>
      <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.chooseImages}>${PlusGlyph({ size: 18 })}<span>Select images</span></button></div>
    <div class="workflow-steps">
      <button class="step-button busy-action" @click=${actions.preview}><b>01</b><span><strong>Preview Plan</strong><small>Validate IDs, categories, and story anchors</small></span></button>
      <button id="apply-button" class="step-button apply-step" disabled @click=${actions.apply}><b>02</b><span><strong>Apply & Place</strong><small>Run 01 Preview Plan first to enable</small></span></button>
      <button class="step-button busy-action" @click=${actions.organizeLoose}><b>03</b><span><strong>Organize Loose Art</strong><small>Sort unplaced root files into category folders</small></span></button>
    </div>
  </section>`
}
