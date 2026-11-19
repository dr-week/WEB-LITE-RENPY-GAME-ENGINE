# LOLA design documents

Central documentation for the LOLA Ren'Py game, Image Workbench, and Python asset pipeline.

- `architecture/TARGET_STRUCTURE.md` — folder ownership across `game/`, `developer-tools/`, and `development/`.
- `architecture/MODULE_RULES.md` — 100-line module limit, ownership, and safety contracts.
- `design/STORY_BIBLE.md` — protagonist Maya, recurring cast, 2–3 meaningful choice rules, Days 1–7 arc, and visual policy.
- `systems/PLAYER_AND_ECONOMY.md` — time slots, attributes (`intelligence`, `appeal`, skills, wellbeing), work, money, and fictional BTC.
- `roadmap/PHASE_ROADMAP.md` — implementation and verification phases.
- `development/WORKBENCH_WORKFLOW.md` — request/asset IDs and end-to-end routing.
- `development/WORKBENCH_SECTIONS.md` — the 5 Workbench sections (`1. Dashboard`–`5. Asset Catalog`) and data owners.
- `development/AUTOMATION_ROADMAP.md` — automated controls and next UI milestones.
- `development/GENERATION_REFRESH.md` — fresh scan and prompt regeneration contract.
- `development/PLAIN_LANGUAGE_AUDIT.md` — `4. Audit & Place` summary and reconciliation flow.
- `development/UNUSED_IMAGE_PLACEMENT_PLAN.md` — picture-to-dialogue placement workflow.
- `assets/ASSET_TAXONOMY.md` — background (`bg_`), story CG (`cg_`), and `reference` categories.
- `assets/FLOW_NAMING.md` — Google Flow naming limits and import convention.
- `assets/VISUAL_METADATA.md` — local visual catalog and caption design.
- `assets/UNUSED_ART_REVIEW.md` — unused art review and story proposal policy.
- `audits/` — current audit reports (`AUDIT_PHASE1.md`, `BLOCKING_ISSUES.md`, `LINT_REPORT_8.6.0_FINAL.md`, `PHASE3_STATUS.md`, `STORY_IMAGE_PLACEMENT_AND_RENPY_LINT_2026-11-15.md`).
- `archive/README.md` — preserved historical project notes and superseded audits.

The ongoing image pipeline lives in modular packages under `developer-tools/`; the desktop GUI lives in `development/image-workbench/`; Ren'Py runtime files live under `game/`.
