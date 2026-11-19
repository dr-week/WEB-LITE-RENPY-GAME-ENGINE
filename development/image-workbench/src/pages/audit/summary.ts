export function auditSummary(output: string): string {
  const indexed = output.match(/Indexed (\d+) image files/)
  if (indexed) return auditResult(output, Number(indexed[1]))
  const catalog = output.match(/Built (\d+) story moments from (\d+) images/)
  if (catalog) return `Rebuilt Maya's City Journal catalog: ${catalog[1]} story moments from ${catalog[2]} images.`
  const preview = output.match(/Dry run: (\d+) placement\(s\), (\d+) for review/)
  if (preview) return previewResult(Number(preview[1]), Number(preview[2]))
  const placed = output.match(/Placed (\d+) image\(s\); (\d+) require/)
  if (placed) return `Added ${placed[1]} picture(s) to the story. ${placed[2]} still need your decision.`
  if (output.startsWith('Running')) return 'Running check on project assets and scripts…'
  if (output.startsWith('Could not')) return 'Refresh failed. Open Scan Details below to see why.'
  return 'Run “Check Script References” or select unplaced art below.'
}

function previewResult(matches: number, review: number): string {
  if (!matches) return `I found ${review} pictures that are not in the story yet, but none have a clear match. Nothing has changed. Choose a story moment for them or save them for later.`
  return `I found ${matches} picture(s) with a story moment that may fit. ${review} more need a decision. Nothing has changed yet; use “Add chosen and matched pictures to story” to continue.`
}

function auditResult(output: string, total: number): string {
  const missingFiles = output.split('\n').filter(line => line.startsWith('MISSING FILE')).length
  const missingNames = output.split('\n').filter(line => line.startsWith('MISSING ALIAS')).length
  if (!missingFiles && !missingNames) return `I checked ${total} picture files. Everything the story asks for is present.`
  const problems = missingFiles + missingNames
  return `I checked ${total} picture files and found ${problems} story picture link(s) that need fixing. Open details below to see which ones.`
}
