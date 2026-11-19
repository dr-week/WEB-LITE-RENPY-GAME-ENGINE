# Google Flow Batch-of-5 Generation & Import Workflow

## Overview
This workflow generates **5 story/replacement images per Flow prompt submission** in the `lolagame` project, tracks per-session counts in `developer-tools/image_audit.sqlite`, and imports downloaded batches with visual QC.

---

## Step-by-Step Pipeline

### 1. Start a Tracked Flow Session
```powershell
$env:PYTHONPATH="developer-tools"
python developer-tools/flow_session.py --start
```

### 2. Generate a 5-Prompt Structured Batch
```powershell
$env:PYTHONPATH="developer-tools"
python developer-tools/prompt_batch.py --limit 5 --format flow-agent --dispatch
```
- Prioritizes `regen` (Thumbs Down / low-quality items) → `story` (`image_requests.json`) → `menu`.
- Outputs **one single message** containing all 5 prompts plus Maya continuity instructions.

### 3. Submit in Google Flow (`lolagame`) — Exact UI Map
- **Project URL**: `https://flow.google.com/project/eed06c76-5b4a-408e-93c1-85b45c395227`
- **Right Agent Panel**:
  1. Click `+` (bottom-left of prompt card) to attach **4–5 Maya reference images** (or select from `Characters` / `Uploads` / `Library`).
  2. Verify sliders icon is set to **16:9** (`Nano Banana 2.1`, `1x` or `2x`).
  3. Click the input with placeholder **`What do you want to create?`**, paste the single 5-prompt message, and click the **`→` arrow button** (bottom-right of the prompt card).
- **Center Grid (Post-Generation)**:
  - Multi-select all newly generated images, add them to a **Library collection** (via `Library +`), and **Download** them directly.

### 4. Log Session Counts & Import Downloads
```powershell
$env:PYTHONPATH="developer-tools"
python developer-tools/flow_session.py --prompts 5 --generated 5 --downloaded 5
python developer-tools/import_collection.py --source "C:\Users\disha\Downloads\<batch_folder>" --apply
python developer-tools/evaluate_story_db.py
```

---

## What Works vs. What Doesn't Work
- **Works**:
  - Sending **5 prompts in one Flow Agent message** with 4–5 Maya reference images attached.
  - Using `prompt_batch.py --dispatch` so `prompt_history` in SQLite prevents duplicate prompt batches.
  - Running `import_collection.py --apply` to validate resolution/sharpness, deduplicate by SHA-256, and rebuild `image_story_catalog.json`.
- **Doesn't Work / Avoid**:
  - Submitting prompts 1-by-1 in the browser (very slow and loses batch context).
  - Generating without Maya reference images (causes outfit/hair drift).
  - Skipping `flow_session.py` counts or `audit_images.py` (leaves `image_audit.sqlite` out of sync).
