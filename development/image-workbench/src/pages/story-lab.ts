import { html, repeat } from '@zuari/dom'
import { state } from '../state'

const THEMES = ['campus_hustle', 'cafe_leverage', 'harbor_twilight', 'library_mystery']

export function storyLabPage(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`<section class="page-stack">
    <div class="overview-grid">
      <article class="content-panel">
        <div class="panel-title"><div><h2>Create 3-Slot Day Arc</h2><p>Generates a 2-option chapter (.rpy) and syncs story_arcs.db.</p></div></div>
        <div class="lab-form">
          <label class="lab-field">Day Number<input id="lab-day-num" type="number" min="8" value="11" /></label>
          <label class="lab-field">Daily Theme<select id="lab-day-theme">${repeat(THEMES, t => t, t => html`<option value=${t}>${t}</option>`)}</select></label>
          <label class="lab-field">Seed (Optional)<input id="lab-day-seed" type="number" placeholder="Random" /></label>
        </div>
        <div class="quick-actions">
          <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.createDay}>Generate Day & Sync DB</button>
        </div>
      </article>
      <article class="content-panel">
        <div class="panel-title"><div><h2>Story Quality & Structure Gate</h2><p>Enforce the strict 2-option rule, label links, and asset integrity.</p></div></div>
        <p class="overview-note">Checks all <code>game/40_story/*.rpy</code> menus, audio symbols, ASCII filenames, and jump targets.</p>
        <div class="quick-actions">
          <button class="zuari-btn busy-action" data-variant="primary" @click=${actions.verifyProject}>Run Full Project Check</button>
          <button class="secondary-btn busy-action" @click=${actions.validateStory}>Validate 2-Option Rule</button>
        </div>
      </article>
    </div>
    <article class="content-panel">
      <div class="panel-title"><div><h2>Lab Output</h2><p>Generation and validation logs</p></div></div>
      <pre class="output-box" aria-live="polite">${state.output}</pre>
    </article>
  </section>`
}
