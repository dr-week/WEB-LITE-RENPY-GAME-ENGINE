export function reconcileConfirmation(output: string): string {
  const rows = output.split('\n').filter(line => line.startsWith('PLACE '))
  const examples = rows.slice(0, 6).map(line => {
    const match = line.match(/^PLACE .+? \| (.+?) -> (.+?) \[/)
    return match ? `• ${match[1]} → ${match[2]}` : ''
  }).filter(Boolean)
  const more = rows.length > examples.length ? `\n…and ${rows.length - examples.length} more` : ''
  return `Add ${rows.length} matched picture(s) to the story?\n\n${examples.join('\n')}${more}\n\nYou can review the changes in the story scripts afterward.`
}
