import { createImportActions } from './imports'
import { createLabActions } from './lab'
import { createNavigationActions } from './navigation'
import { createProjectActions } from './project'
import { assignStagedImage } from './metadata'

export function createActions() {
  return {
    ...createImportActions(),
    ...createLabActions(),
    ...createNavigationActions(),
    ...createProjectActions(),
    assignImage: assignStagedImage
  }
}
