import { html } from '@zuari/dom'
import { state } from '../state'
import { uploadPanel } from './intake/upload-panel'
import { stagedAssets } from './intake/staged-assets'

export function intakePage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    ${uploadPanel(actions)}
    ${stagedAssets(actions)}
    <details open class="content-panel"><summary class="panel-summary">Execution Log</summary>
      <pre class="output-box intake-output" aria-live="polite">${state.output}</pre>
    </details>
  </section>`
}
