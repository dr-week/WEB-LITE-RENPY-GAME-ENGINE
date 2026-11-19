import { state } from './state'

export function showError(error: unknown): void {
  state.status.value = 'Action failed'
  state.output.value = error instanceof Error ? error.message : String(error)
}
