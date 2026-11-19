# LOLA Architecture and Work Plan

## Purpose

This folder contains the implementation plan, feature-specific design notes,
and asset mapping for the Ren'Py project. Runtime features remain native
Ren'Py; no web framework is part of the game runtime.

## Documents by function

| Document | Function |
|---|---|
| [MODULAR_REBUILD_PLAN.md](./MODULAR_REBUILD_PLAN.md) | Architecture conventions and validation gates |
| [ASSET_STORY_MAP.md](./ASSET_STORY_MAP.md) | Existing artwork mapping and story placement rules |
| [PHASE_01_FOUNDATION.md](./PHASE_01_FOUNDATION.md) | Runtime, entry flow, compatibility, and tests |
| [PHASE_02_UI.md](./PHASE_02_UI.md) | Menus, settings, save/load, accessibility and visual polish |
| [PHASE_03_STORY_ASSETS.md](./PHASE_03_STORY_ASSETS.md) | Narrative structure and image integration |
| [PHASE_04_MODULARITY.md](./PHASE_04_MODULARITY.md) | Small-file rule, refactoring sequence, and ongoing checks |

## Order of work

1. Finish Phase 1 gates and make the UI test suite reliable.
2. Refine Phase 2 based on a visual playthrough.
3. Inventory and assign assets as part of Phase 3.
4. Refactor existing oversized code files incrementally under Phase 4; keep
   each refactor behavior-preserving and lint/test it before moving on.

## Source file size rule

Every code file must contain **fewer than 100 lines**. Keep source files below
that ceiling by splitting along a single responsibility: one screen, one
focused manager, one short story scene, or one test concern. Count blank and
comment lines too. Documentation is organized by function but is not subject
to the source-code line limit.

Existing violations are listed in [PHASE_04_MODULARITY.md](./PHASE_04_MODULARITY.md)
and must be removed before the codebase is considered compliant.
