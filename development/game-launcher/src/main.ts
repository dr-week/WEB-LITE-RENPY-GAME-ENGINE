import './styles.css'
import { invoke } from '@tauri-apps/api/core'
import { open } from '@tauri-apps/plugin-dialog'

interface LauncherState {
  version: string
  sdk: string
  mode: string
  fullscreen: boolean
  hero_data_url: string | null
  game_running: boolean
}

const MODES = ['Auto (Recommended)', 'ANGLE / DirectX', 'Software (No GPU)']

async function boot() {
  const app = document.querySelector<HTMLElement>('#app')!
  const state = await invoke<LauncherState>('get_launcher_state')
  app.innerHTML = `
    <main class="shell">
      <aside class="hero">
        ${state.hero_data_url ? `<img src="${state.hero_data_url}" alt="LOLA" />` : ''}
        <span class="hero-badge">v${state.version}</span>
      </aside>
      <section class="panel">
        <div>
          <h1 class="title">LOLA</h1>
          <p class="subtitle">A New City, A New Beginning</p>
          <p class="tagline">Balance college, work, friendships, and city hustle as Maya.</p>
          <button id="play" class="play-btn">${state.game_running ? 'LOLA Already Running' : 'Play LOLA'}</button>
          <div class="glass-box">
            <label class="check-row"><input id="fs" type="checkbox" ${state.fullscreen ? 'checked' : ''} /><span>Start Fullscreen</span></label>
            <label class="field-label">Display Renderer
              <select id="mode">${MODES.map(m => `<option value="${m}" ${m === state.mode ? 'selected' : ''}>${m}</option>`).join('')}</select>
            </label>
          </div>
          <p id="status" class="status">${state.sdk ? '' : 'Ren\'Py SDK not found — locate it below.'}</p>
        </div>
        <footer class="footer">
          <button id="sdk" class="ghost-btn">${state.sdk ? 'Change SDK…' : 'Locate Ren\'Py SDK…'}</button>
          <button id="exit" class="ghost-btn">Exit</button>
        </footer>
      </section>
    </main>`

  const status = document.querySelector<HTMLElement>('#status')!
  const fs = document.querySelector<HTMLInputElement>('#fs')!
  const mode = document.querySelector<HTMLSelectElement>('#mode')!
  const play = document.querySelector<HTMLButtonElement>('#play')!

  const save = () => invoke('save_launcher_settings', { mode: mode.value, fullscreen: fs.checked, sdk: null })
  fs.addEventListener('change', () => { void save() })
  mode.addEventListener('change', () => { void save() })

  play.addEventListener('click', async () => {
    play.disabled = true
    status.textContent = 'Starting LOLA…'
    try {
      await save()
      await invoke('launch_lola_game')
    } catch (err) {
      status.textContent = String(err)
      play.disabled = false
    }
  })

  document.querySelector('#sdk')!.addEventListener('click', async () => {
    const folder = await open({ directory: true, multiple: false })
    if (typeof folder === 'string') {
      await invoke('save_launcher_settings', { mode: mode.value, fullscreen: fs.checked, sdk: folder })
      status.textContent = 'Ren\'Py SDK saved.'
    }
  })
  document.querySelector('#exit')!.addEventListener('click', () => { void invoke('exit_launcher') })
}

void boot()
