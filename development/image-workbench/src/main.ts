import '@zuari/theme'
import './styles.css'
import { getCurrentWebview } from '@tauri-apps/api/webview'
import { createActions } from './actions/index'
import { mountView } from './view'
import { browserPreview } from './preview/mode'

const root = document.querySelector<HTMLElement>('#app')
if (!root) throw new Error('Workbench application root is missing.')

const actions = createActions()
const dispose = mountView(root, actions)
window.addEventListener('beforeunload', dispose, { once: true })
if (!browserPreview) {
  void getCurrentWebview().onDragDropEvent(({ payload }) => {
    if (payload.type === 'drop') void actions.dropFiles(payload.paths)
  }).catch(actions.showError)
}
void actions.boot()
