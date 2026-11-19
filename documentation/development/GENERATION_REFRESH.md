# Generation list refresh

## UI behavior

Generation List now has an explicit **Refresh list** control. It runs the local
story image scanner and rebuilds both the Markdown report and structured
`image_requests.json` from the current story and registered assets. The global
navigation entry also refreshes the list.

## Freshness contract

- A request is a need, not merely an image filename.
- Keep a need visible while its beat is unplaced; remove it after the script
  uses the appropriate image alias.
- Existing tagged images appear as **Existing art to review**, separate from
  fresh generation needs; Asset Audit remains the full inventory view.
- Refresh is read-only with respect to story scripts and image files.
- Show scan errors instead of presenting an old report as fresh.

## Verification checklist

1. Add a new dialogue beat and refresh: one new request appears.
2. Refresh again without changes: no duplicate request appears.
3. Import and place an image for that beat, then refresh: the need disappears.
4. Keep a generated image unplaced: it remains visible in unused-art review.
5. Change story dialogue: the old request ID is rejected as stale.
