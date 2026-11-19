# Visual image metadata catalog

## Goal

Make image contents searchable without guessing from filenames. Keep story
placement separate from visual description: a caption describes pixels; a
`story_key` identifies the dialogue request.

## Lightweight design

- Canonical record: same-stem JSON sidecar next to each image.
- Search/index: rebuildable SQLite database under the development app's local
  data directory; store paths, hashes, captions, tags, and review state, not
  duplicate image bytes.
- Scan: extract dimensions, format, size, file hash, and embedded metadata.
- Optional local AI pass: draft a one-sentence caption and structured tags.
  Human edits win; store model name, version, and timestamp for provenance.
- Search v1: SQLite full-text search across filename, caption, tags, prompt, and
  Flow metadata. Add vector similarity only if keyword search proves inadequate.

## Suggested fields

`asset_id`, `path`, `caption`, `subjects`, `actions`, `setting`, `mood`,
`composition`, `tags`, `width`, `height`, `format`, `source_prompt`,
`source_media_id`, `story_key`, `placement_status`, `description_status`,
`description_model`, `description_updated_at`, `human_notes`.

Use `unknown` when uncertain. Keep generated captions marked `draft` until a
person reviews them. Never use a visual model's guess as an automatic story
target.

## Existing project references

- [qimg](https://github.com/idanariav/qimg): local captions and hashes, SQLite,
  keyword plus embedding search; useful architecture reference.
- [ImageArc](https://github.com/robouden/imagearc): local Ollama captioning and
  IPTC/XMP metadata; useful interoperability reference.
- [PhotoSearch](https://github.com/giuvilas/Local-aiPhotos): plain JSONL index,
  local vision model, no vector database; useful simple-index reference.

The first increment should be technical metadata plus editable caption/tags.
Choose a model and hardware target only after measuring scan time on this PC.
