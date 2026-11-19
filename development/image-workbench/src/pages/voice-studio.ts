import { html } from '@zuari/dom'
import { state } from '../state'

export function voiceStudioPage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    <div class="overview-grid">
      <article class="content-panel">
        <div class="panel-title"><div><h2>Maya Cute Gen-Z Voice & TTS</h2><p>Synthesize dialogue lines and emotional harmonic mumbles.</p></div></div>
        <p class="overview-note">Uses <code>en-US-AnaNeural</code> (when <code>edge-tts</code> is installed) or offline Windows SAPI5, with 8 harmonic mumble fallbacks.</p>
        <div class="quick-actions">
          <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.voiceStatus}>Check Voice Coverage</button>
          <button class="secondary-btn busy-action" @click=${actions.voiceScan}>Scan Story Lines</button>
        </div>
      </article>
      <article class="content-panel">
        <div class="panel-title"><div><h2>Audio Generation Batch</h2><p>Pre-render missing spoken clips and refresh mumble profiles.</p></div></div>
        <p class="overview-note">Emotions: <code>neutral</code>, <code>happy</code>, <code>proud</code>, <code>hopeful</code>, <code>teasing</code>, <code>shy</code>, <code>tired</code>, <code>worried</code>.</p>
        <div class="quick-actions">
          <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.voiceSynth}>Synth Missing TTS (10)</button>
          <button class="secondary-btn busy-action" @click=${actions.voiceMumbles}>Regenerate 8 Mumbles</button>
        </div>
      </article>
    </div>
    <article class="content-panel">
      <div class="panel-title"><div><h2>Voice Studio Output</h2><p>Coverage breakdown and synthesized clip paths</p></div></div>
      <pre class="output-box" aria-live="polite">${state.output}</pre>
    </article>
  </section>`
}
