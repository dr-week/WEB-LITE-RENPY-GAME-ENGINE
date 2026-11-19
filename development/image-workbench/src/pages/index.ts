import { intakePage } from './intake'
import { generationPage } from './generation'
import { auditPage } from './audit'
import { imageDataPage } from './image-data'
import { overviewPage } from './overview'
import { storyLabPage } from './story-lab'
import { voiceStudioPage } from './voice-studio'

export function pageContent(section: string, actions: ReturnType<typeof import('../actions').createActions>) {
  if (section === 'overview') return overviewPage(actions)
  if (section === 'generation') return generationPage(actions)
  if (section === 'audit') return auditPage(actions)
  if (section === 'data') return imageDataPage(actions)
  if (section === 'story') return storyLabPage(actions)
  if (section === 'voice') return voiceStudioPage(actions)
  return intakePage(actions)
}
