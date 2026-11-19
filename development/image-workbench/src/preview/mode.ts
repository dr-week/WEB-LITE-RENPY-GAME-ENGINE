export const browserPreview = new URLSearchParams(location.search).get('preview') === 'browser'
const requestedSection = new URLSearchParams(location.search).get('section')
const validSections = ['overview', 'intake', 'generation', 'audit', 'data']
export const initialSection = browserPreview && requestedSection && validSections.includes(requestedSection)
  ? requestedSection
  : 'overview'
