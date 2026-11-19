# Modular development roadmap

## Phase 0 — baseline and contracts

Record labels, screens, image aliases, state fields, save behavior, and current
tests. Confirm Maya, starting money, city setting, and story tone in the bible.

**Progress:** Design documents and core contract are in place. Maya, starting
cash, no-sprite visual policy, and the weekday loop are documented.

## Phase 1 — structure

Consolidate project documentation outside `game/`. Move one `.rpy` responsibility
at a time into the target subfolders. Preserve labels/aliases and check load order.
Retire duplicate time/day helper definitions after choosing one canonical owner.

**Progress:** `00_systems` is split by responsibility, GUI fragments are under
`30_screens/theme/`, and historical notes are archived outside `game/`.
Duplicate time helpers were removed; Ren'Py lint passes after the moves.

## Phase 2 — save-safe player state

Define and document skill, wellbeing, mood, wallet, job, calendar, and ledger
fields. Add new-save defaults and old-save migration before exposing new screens.

**Progress:** Skills, mood, wallet ledger, portfolio, work, and study counters
now have Ren'Py defaults. Old saves receive defaults for newly introduced fields.

## Phase 3 — playable systems

Wire education, job shifts, expenses, and offline BTC investment into one day
loop. Add a compact transaction history and accessible stats/finance screens.

**Progress:** Offline BTC buy/sell, wallet history recording, stat hooks, finance
choices, status values, day summary, and single-application shift costs are wired.
Full ledger browsing and broader story branches remain future work.

## Phase 4 — story expansion (COMPLETE)

Built a complete Days 1–7 Week 1 arc (`day_router.rpy`, `day_01_*` prologue, `day_02_class.rpy` through `day_06_weekend.rpy`, shared 3-pillar `day_hub.rpy`, `week_01_evaluation`, and open Week 2 `day_free_morning.rpy`). Every story and location menu follows the 2–3 choice rule and awards meaningful stats (`intelligence`, `appeal`, skills, `money`, wellbeing, or relationships).

## Phase 5 — image pipeline & Workbench UI (COMPLETE)

Modularized `developer-tools/` into clean Python subpackages (`image_generation/`, `image_import/`, `image_reconciliation/`, `image_audit/`, `image_story_loop/`, `tests/`), renamed non-ASCII artwork to ASCII-safe filenames, organized loose `game/images/` files, wired additional `cg_*` art into Days 1–5, and streamlined LOLA Workbench into 5 numbered sections (`1. Dashboard`–`5. Asset Catalog`) without duplicated headings or cards.

## Phase 6 — validation & documentation sync (COMPLETE)

Verified all 164 active source files stay `<= 100` lines, Ren'Py `8.6.0` lint passes with exit code 0 and zero warnings, Python unit tests and Tauri Rust unit tests pass, and all documentation is synchronized with the codebase.

## Exit gates

- [x] No duplicate state owners, missing labels/aliases, or code files over 100 lines.
- [x] Curated image rules, audit SQLite DB, and City Journal catalog stay synced.
- [x] Every story branch reaches a valid daytime hub or `end_day` progression exit.
