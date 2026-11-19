import { html, render } from '@zuari/dom'
import { effect } from '@zuari/signals'
import { pageContent } from './pages'
import { navigation } from './ui/navigation'
import { state } from './state'
import { browserPreview } from './preview/mode'

const titles: Record<string, string> = {
  overview: '1. Dashboard',
  intake: '2. Stage & Route',
  generation: '3. Story Prompts',
  audit: '4. Audit & Place',
  data: '5. Asset Catalog',
  story: '6. Story & Day Lab',
  voice: '7. Voice & Audio Studio'
}

const subtitles: Record<string, string> = {
  overview: 'Unified inventory health, pipeline stages, and quick maintenance actions.',
  intake: 'Drop new art into intake, bind to a request or category, preview, and apply.',
  generation: 'Fresh dialogue prompts from unillustrated beats with character references.',
  audit: 'Verify Ren\'Py script references and bind unplaced art to exact story lines.',
  data: 'Categorized asset inventory, placement status, and request tracking.',
  story: 'Generate creative 3-slot Day arcs, sync SQLite DB, and enforce 2-option rules.',
  voice: 'Inspect Maya Gen-Z voice coverage, synthesize TTS clips, and tune emotional mumbles.'
}

export function mountView(root: HTMLElement, actions: ReturnType<typeof import('./actions').createActions>): () => void {
  const view = render(html`
    <main class="zuari-app-canvas app-shell" data-zuari-theme="studio">
      <aside id="sidebar-host" class="sidebar"></aside>
      <section class="main-content">
        <header class="topbar"><div><p class="zuari-editorial-eyebrow">LOLA WORKBENCH</p><h1 class="zuari-editorial-title">${() => titles[state.activeSection.value] || titles.overview}</h1><p class="topbar-subtitle">${() => subtitles[state.activeSection.value] || subtitles.overview}</p></div>
          <div class="topbar-actions">
            <span class="busy-pill" style=${() => state.busy.value ? '' : 'display:none'}>Working…</span>
            <button class="secondary-btn busy-action" @click=${actions.refreshInventory}>Refresh</button>
            <span class="zuari-tag-pill native-badge">${browserPreview ? 'BROWSER PREVIEW' : 'TAURI DESKTOP'}</span>
          </div></header>
        <div id="active-page"></div>
        <footer class="footer"><span>${state.status}</span><small>${state.projectRoot}</small></footer>
      </section>
    </main>`, root)
  const sidebar = root.querySelector<HTMLElement>('#sidebar-host')!
  const nav = render(navigation(actions), sidebar)
  const host = root.querySelector<HTMLElement>('#active-page')!
  let page: ReturnType<typeof render> | undefined
  const stopPage = effect(() => {
    const section = state.activeSection.value
    page?.destroy()
    host.replaceChildren()
    page = render(pageContent(section, actions), host)
    syncActionButtons(host)
  })
  const stopBusy = effect(() => {
    const busy = state.busy.value
    root.querySelectorAll<HTMLButtonElement>('.busy-action').forEach(b => { b.disabled = busy })
    syncActionButtons(root)
  })
  return () => { stopPage(); stopBusy(); page?.destroy(); nav.destroy(); view.destroy() }
}

function syncActionButtons(scope: HTMLElement) {
  const busy = state.busy.value
  const apply = scope.querySelector<HTMLButtonElement>('#apply-button')
  const reconcile = scope.querySelector<HTMLButtonElement>('#reconcile-apply-button')
  if (apply) apply.disabled = busy || !state.canApply.value
  if (reconcile) reconcile.disabled = busy || !state.canReconcileApply.value
}
