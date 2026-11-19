import { html } from '@zuari/dom'
import { SparkleGlyph } from '@zuari/glyphs/actions'
import { CheckGlyph, PlusGlyph } from '@zuari/glyphs/icons'
import { GridGlyph } from '@zuari/glyphs/navigation'
import { createSvgElement } from '@zuari/glyphs/base'
import { state } from '../state'

const OverviewGlyph = createSvgElement('0 0 24 24', '<path d="M4 19V5M4 19h17"/><path d="m7 15 4-4 3 2 6-7"/>')
const StoryGlyph = createSvgElement('0 0 24 24', '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>')
const VoiceGlyph = createSvgElement('0 0 24 24', '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/>')
const openPrompts = () => state.requests.value.filter(r => r.status === 'needs_generation').length

export function navigation(actions: ReturnType<typeof import('../actions').createActions>) {
  return html`
    <div class="sidebar-content">
      <div class="brand">${SparkleGlyph({ size: 23 })}<span>LOLA <small>DEV WORKBENCH</small></span></div>
      <nav class="workflow-nav" aria-label="Artwork Pipeline">
        <p class="nav-caption">ARTWORK PIPELINE</p>
        <button class=${() => state.activeSection.value === 'overview' ? 'nav-item active' : 'nav-item'} @click=${actions.showOverview}>${OverviewGlyph}<span>1. Dashboard</span></button>
        <button class=${() => state.activeSection.value === 'intake' ? 'nav-item active' : 'nav-item'} @click=${actions.showImageIntake}>${PlusGlyph({ size: 17 })}<span>2. Stage & Route</span><b class="nav-badge" style=${() => Number(state.rootImages.value) ? '' : 'display:none'}>${state.rootImages}</b></button>
        <button class=${() => state.activeSection.value === 'generation' ? 'nav-item active' : 'nav-item'} @click=${actions.showGeneration}>${SparkleGlyph({ size: 17 })}<span>3. Story Prompts</span><b class="nav-badge" style=${() => openPrompts() ? '' : 'display:none'}>${openPrompts}</b></button>
        <button class=${() => state.activeSection.value === 'audit' ? 'nav-item active' : 'nav-item'} @click=${actions.showAudit}>${CheckGlyph({ size: 17 })}<span>4. Audit & Place</span><b class="nav-badge" style=${() => Number(state.unusedImages.value) ? '' : 'display:none'}>${state.unusedImages}</b></button>
        <button class=${() => state.activeSection.value === 'data' ? 'nav-item active' : 'nav-item'} @click=${actions.showImageData}>${GridGlyph({ size: 17 })}<span>5. Asset Catalog</span></button>
      </nav>
      <nav class="workflow-nav" aria-label="Story and Voice">
        <p class="nav-caption">STORY & VOICE LAB</p>
        <button class=${() => state.activeSection.value === 'story' ? 'nav-item active' : 'nav-item'} @click=${actions.showStoryLab}>${StoryGlyph}<span>6. Story & Day Lab</span></button>
        <button class=${() => state.activeSection.value === 'voice' ? 'nav-item active' : 'nav-item'} @click=${actions.showVoiceLab}>${VoiceGlyph}<span>7. Voice & Audio</span></button>
      </nav>
      <div class="nav-tools">
        <p class="nav-caption">DOCS & TOOLS</p>
        <button class="tool-link" @click=${actions.openStoryBible}>Story Bible</button>
        <button class="tool-link" @click=${actions.openRoadmap}>Roadmap</button>
        <button class="tool-link" @click=${actions.openStoryProposals}>Scene Proposals</button>
        <button class="tool-link" @click=${actions.openGuide}>Import Guide</button>
        <button class="tool-link" @click=${actions.openTemplate}>Metadata Template</button>
      </div>
      <div class="sidebar-bottom">
        <span class="nav-caption">PROJECT ROOT</span>
        <button class="root-button" title=${state.projectRoot} @click=${actions.chooseProject}>${state.projectRoot}</button>
      </div>
    </div>`
}
