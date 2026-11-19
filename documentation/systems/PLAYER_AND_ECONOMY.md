# Player and economy systems

## State ownership

Use one saved profile with a canonical display name (currently Maya), one
wallet, one calendar, and one owner for each statistic. Initialize all mutable
playthrough fields with Ren'Py `default`; migrate new fields safely into old saves.

## Suggested stat groups

- **Core attributes, 0–100**: `intelligence` (analytical sharpness, class/study mastery) and `appeal` (poise, warmth, social presence), alongside `confidence` and `reputation`.
- **Practical skills, 0–100**: `learning`, `communication`, `work_skill`, and `financial_literacy`.
- **Wellbeing, 0–100**: `energy`, `stress`, and `health`.
- **Mood**: a short-lived state (`calm`, `anxious`, `hopeful`, `embarrassed`, `tired`, or `proud`).
- **Social progress**: per-character `friendship`, `romance`, and `hostility` values, gated cleanly in `character_info` to introduced characters.

Every choice modifies a documented subset of attributes, skills, cash, wellbeing, or relationships.

## Day and work loop

`morning` chapter beat → `afternoon` / `evening` 3-pillar hub (`day_hub.rpy`: **Study**, **Work**, or **City Life & Journal**) → `night` wrap (`end_day_home` → `end_day`). Actions consume a time slot via `day_hub_after_activity`; `start_new_day()` advances the day once, and `work_shift()` applies wage/energy/skill updates once per shift.

## Money and investment

- Keep the current 120-dollar balance as a provisional starting value.
- Record earnings, purchases, and bills in `wallet_ledger` through `wallet_manager.rpy`.
- Model Bitcoin as an offline, story-day-scheduled in-game holding (`bitcoin_units`, `bitcoin_cost_basis`, `bitcoin_realized_gain`).
- Provide $0 alternatives wherever choices spend cash so low-balance runs stay playable.

## Implemented modules

- `game/00_systems/core/state.rpy` & `state_init.rpy` own save-backed defaults, `init_new_game_state()`, and initial cast setup.
- `game/00_systems/player/stats_manager.rpy` owns bounded attribute, skill, wellbeing, and mood updates via `change_stat()`.
- `game/00_systems/education/college_manager.rpy` grows `education_progress`, `learning`, and `intelligence` across classes, library study, and assignments.
- `game/00_systems/economy/wallet_manager.rpy` & `investment_manager.rpy` own cash changes, ledger history, and fictional BTC pricing.
- `game/00_systems/time/time_manager.rpy` owns the single day transition and overnight recovery.
- `game/30_screens/status.rpy` & `character_info.rpy` expose all stats, `intelligence`/`appeal`, BTC value, and introduced relationships from both the quick menu and game menu.
