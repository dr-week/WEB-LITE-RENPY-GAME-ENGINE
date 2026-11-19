# LOLA System Dependency Map

**Date:** 2026-11-13
**Version:** 0.6

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        game/script.rpy                          │
│                    (Entry point, lifecycle)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  00_systems/state.rpy                           │
│         (Core state, protagonist config, defaults)              │
│         Depends on: nothing (foundational)                      │
│         Called by: all systems, story files                    │
└─────────────────────────────────────────────────────────────────┘
              │              │              │              │
              ▼              ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ 10_characters/│ │ relationship │ │ encounter_   │ │ location_    │
    │ character_    │ │ _manager.rpy │ │ manager.rpy  │ │ manager.rpy  │
    │ _registry.rpy │ ├──────────────┤ ├──────────────┤ ├──────────────┤
    ├──────────────┤ │ State:       │ │ State:       │ │ State:       │
    │ State:        │ │ - None       │ │ - None       │ │ - locations   │
    │ - IDs         │ │              │ │              │ │ - travel     │
    │ - lookup      │ │ Functions:   │ │ Functions:   │ │              │
    │               │ │ - update_    │ │ - generate_  │ │ Functions:   │
    │ Functions:    │ │   relationship│ │   encounter  │ │ - get_location│
    │ - register    │ │ - get_level  │ │ - promote    │ │ - travel_to  │
    │ - get_by_id   │ │ - get_summary│ │ - can_recur  │ │ - unlock     │
    │ - get_all     │ │              │ │              │ │              │
    │ - generate_   │ │ Depends on:  │ │ Depends on:  │ │ Depends on:  │
    │   name        │ │ - character  │ │ - character  │ │ - state.rpy  │
    │               │ │   _registry  │ │   _registry  │ │              │
    │ Depends on:   │ │              │ │              │ │ Called by:   │
    │ - state.rpy   │ │ Called by:   │ │ Called by:   │ │ - story files│
    │               │ │ - encounter  │ │ - story files│ │ - location   │
    │ Called by:    │ │   _manager   │ │ - character  │ │   files      │
    │ - all systems │ │ - story      │ │   _registry  │ │              │
    │ - story       │ │   files      │ │              │ │              │
    │   files       │ └──────────────┘ └──────────────┘ └──────────────┘
    └──────────────┘               │              │              │
              │                   ▼              ▼              ▼
              ▼             ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    ┌──────────────┐         │ economy_     │ │ time_        │ │ college_     │
    │ 10_characters/│         │ manager.rpy  │ │ manager.rpy  │ │ manager.rpy  │
    │ recurring_    │         ├──────────────┤ ├──────────────┤ ├──────────────┤
    │ _cast.rpy     │         │ State:       │ │ State:       │ │ State:       │
    ├──────────────┤         │ - money      │ │ - time_slot  │ │ - progress   │
    │ State:        │         │ - currency   │ │ - day        │ │ - course     │
    │ - Authored    │         │              │ │              │ │ - assignments│
    │   characters  │         │ Functions:   │ │ Functions:   │ │              │
    │               │         │ - add/spend  │ │ - advance    │ │ Functions:   │
    │ Functions:    │         │   _money     │ │   _slot      │ │ - attend     │
    │ - is_         │         │ - can_       │ │ - start_day  │ │   _class     │
    │   _character_ │         │   _afford    │ │              │ │ - study      │
    │   _introduced │         │ - format_    │ │ - get_day_   │ │   _library   │
    │ - get_        │         │   _money     │ │   _info      │ │              │
    │   _recurring_ │         │              │ │              │ │ Depends on:  │
    │   _count      │         │ Depends on:  │ │ Depends on:  │ │ - state.rpy  │
    │               │         │ - state.rpy  │ │ - state.rpy  │ │              │
    │ Depends on:   │         │              │ │              │ │ Called by:   │
    │ - state.rpy   │         │ Called by:   │ │ Called by:   │ │ - story files│
    │               │         │ - story files│ │ - story files│ │              │
    │ Called by:    │         │ - location   │ │ - economy    │ │              │
    │ - story files │         │   files      │ │   _manager   │ │              │
    └──────────────┘         │              │ │              │ │              │
              │               └──────────────┘ └──────────────┘ └──────────────┘
              ▼                      │              │              │
              ▼             ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    ┌──────────────┐         │ employment_  │ │              │ │ 50_world_map/│
    │ 10_characters/│         │ manager.rpy  │ │              │ │ world_map.rpy │
    │ generated_    │         ├──────────────┤ │              │ │ (Location    │
    │ _encounters.r │         │ State:       │ │              │ │  data only)  │
    │ py            │         │ - job        │ │              │ │              │
    ├──────────────┤         │ - shifts     │ │              │ │ Depends on:  │
    │ State:        │         │ - experience │ │              │ │ - state.rpy  │
    │ - encounter   │         │              │ │              │ │              │
    │   types       │         │ Functions:   │ │              │ │ Called by:   │
    │               │         │ - start_     │ │              │ │ - location   │
    │ Functions:    │         │   _job       │ │              │ │   files      │
    │ - encounter_  │         │ - work_      │ │              │ │              │
    │   _types      │         │   _shift     │ │              │ │              │
    │ - create_     │         │ - get_       │ │              │ │              │
    │   _encounter  │         │   _earnings  │ │              │ │              │
    │ - promote_    │         │              │ │              │ │              │
    │   _to_        │         │ Depends on:  │ │              │ │              │
    │   _recurring  │         │ - state.rpy  │ │              │ │              │
    │               │         │              │ │              │ │              │
    │ Depends on:   │         │ Called by:   │ │              │ │              │
    │ - state.rpy   │         │ - story files│ │              │ │              │
    │ - character_  │         │ - location   │ │              │ │              │
    │   _registry   │         │   files      │ │              │ │              │
    │               │         └──────────────┘ └──────────────┘ └──────────────┘
    │ Called by:    │               │              │              │
    │ - story files │               ▼              ▼              ▼
    └──────────────┘         ┌──────────────┐
              │             │ event_       │
              ▼             │ manager.rpy  │
    ┌──────────────┐         ├──────────────┤
    │ 30_screens/   │         │ State:       │
    │ navigation.r  │         │ - recent_    │
    │ py            │         │   events     │
    ├──────────────┤         │ - day_       │
    │ Screens:      │         │   summary    │
    │ - world_map   │         │              │
    │ - status      │         │ Functions:   │
    │ - character   │         │ - record_    │
    │   _info       │         │   event      │
    │ - custom_     │         │ - get_recent │
    │   _choices    │         │ - has_event  │
    │               │         │ - get_events │
    │ Depends on:   │         │   _for_      │
    │ - 00_systems/ │         │   _character│
    │   *_manager   │         │ - record_    │
    │               │         │   _day_      │
    │ Called by:    │         │   _summary   │
    │ - script.rpy  │         │ - clear_     │
    │ - story files │         │   _recent    │
    │               │         │   _events    │
    │               │         │              │
    │               │         │ Depends on:  │
    │               │         │ - state.rpy  │
    │               │         │              │
    │               │         │ Called by:   │
    │               │         │ - story files│
    │               │         │ - location   │
    │               │         │   files      │
    └──────────────┘         └──────────────┘
              │
              ▼
    ┌──────────────┐
    │ script.rpy   │
    │ (Entry point)│
    └──────────────┘
```

## Module Details

### 1. 00_systems/state.rpy
**Responsibility:** Core game state, protagonist configuration, foundational defaults
**State owned:**
- `protagonist` dict (name, age, is_adult, pronouns, etc.)
- `current_day`, `time_slot`, `game_state`
- `current_location`, `traveled_to`, `available_locations`
- `reputation`, `relationship_count`
- `energy`, `stress`, `confidence`, `health`
- `education_progress`, `has_college_id`, `college_course`
- `assignments_due`, `classes_attended`
- `employment_state`, `current_job`, `shift_today`, `work_experience`
- `recurring_characters`, `generated_characters`, `used_names`
- `story_flags`, `recent_events`, `day_summary`
- `money`, `currency`, `essential_costs`

**Public functions:**
- `get_status_summary()` - readable state summary
- `set_flag()`, `get_flag()`, `has_flag()` - story flag management
- `add_recent_event()` - event logging
- `advance_time_slot()`, `start_new_day()` - time progression
- `record_day_summary()` - day summary logging
- `get_character_count()` - character count
- `is_protagonist_adult()` - adult check

**Dependencies:** None (foundational)
**Called by:** All systems, all story files
**Rollback/save:** All state uses `default` - safe for rollback

---

### 2. 10_characters/character_registry.rpy
**Responsibility:** Character ID management, name generation, lookup
**State owned:**
- Uses `recurring_characters`, `generated_characters`, `used_names` from state.rpy

**Public functions:**
- `generate_name(gender)` - unique name generation
- `register_recurring_character(id, data)` - register authored character
- `get_character_by_id(id)` - lookup by ID
- `get_all_characters()` - get all characters
- `get_character_count()` - count characters
- `remove_generated_character(id)` - cleanup
- `list_characters_by_role(role)` - filter by role

**Dependencies:** state.rpy (for character dicts and used_names)
**Called by:** encounter_manager.rpy, relationship_manager.rpy, all story files
**Rollback/save:** Names generated once - stored in used_names set. Safe if set is rollback-aware.

---

### 3. 10_characters/relationship_manager.rpy
**Responsibility:** Per-character relationship tracking (friendship/romance/hostility)
**State owned:**
- Uses character records from character_registry.rpy

**Public functions:**
- `update_relationship(character_id, type, amount, bounded)` - modify relationship
- `get_relationship_level(value)` - value to text conversion
- `get_relationship_description(character_id)` - readable description
- `get_strongest_relationship(character_id)` - dominant relationship type
- `can_characters_interact(id1, id2)` - interaction check
- `get_relationship_summary_for_character(character_id)` - full summary
- `is_relationship_meaningful(character_id)` - has meaningful relationship

**Dependencies:** character_registry.rpy (for character lookup)
**Called by:** encounter_manager.rpy, all story files
**Rollback/safe:** Relationship values stored in character dicts. Must use default/rollback-safe state.

---

### 4. 10_characters/encounter_manager.rpy
**Responsibility:** Generated encounter creation, promotion to recurring
**State owned:**
- Uses `generated_characters`, `used_names` from state.rpy
- Uses name generation from character_registry.rpy

**Public functions:**
- `generate_encounter_character(scene_type, venue, gender_preference)` - create new encounter
- `promote_to_recurring(character_id, recurring_role, recurring_name)` - promote to recurring
- `can_character_recur(character_id)` - check recurrence eligibility
- `record_character_event(character_id, event_type)` - log event
- `get_character_summary(character_id)` - readable summary

**Dependencies:** character_registry.rpy (for name generation and registry)
**Called by:** All story files (when creating encounters)
**Rollback/save:** CRITICAL - encounter creation must happen once. Random IDs must be stable across save/load.

---

### 5. 00_systems/location_manager.rpy
**Responsibility:** Location data, travel logic, location availability
**State owned:**
- `locations` dict (location definitions)
- Uses `current_location`, `traveled_to` from state.rpy

**Public functions:**
- `get_location(loc_id)` - get location data
- `get_location_name(loc_id)` - display name
- `is_location_available(loc_id)` - availability check
- `is_location_unlocked(loc_id)` - visited check
- `travel_to(location_id)` - travel execution
- `unlock_location(location_id)` - mark as visited
- `get_available_locations()` - list available
- `get_location_description(loc_id)` - description text
- `can_afford_location(loc_id)` - cost check

**Dependencies:** state.rpy (for current_location, traveled_to, money)
**Called by:** All location files, story files
**Rollback/save:** Location state uses defaults - safe.

---

### 6. 00_systems/economy_manager.rpy
**Responsibility:** Money management, costs, transactions
**State owned:**
- Uses `money`, `currency`, `essential_costs` from state.rpy

**Public functions:**
- `add_money(amount)` - add funds
- `spend_money(amount)` - spend funds (returns success)
- `can_afford(amount)` - affordability check
- `get_balance()` - current balance
- `daily_expenses()` - apply daily costs
- `set_essential_cost(category, amount)` - set cost
- `get_essential_costs()` - get all costs
- `format_money(amount)` - display formatting

**Dependencies:** state.rpy (for money, currency)
**Called by:** All story files, location files, employment_manager.rpy
**Rollback/save:** Money changes must be explicit and reversible.

---

### 7. 00_systems/time_manager.rpy
**Responsibility:** Day and time slot progression
**State owned:**
- Uses `current_day`, `time_slot` from state.rpy

**Public functions:**
- `get_current_time_slot()` - current slot
- `advance_time_slot()` - next slot
- `go_to_time_slot(slot)` - set specific slot
- `is_time_slot(slot)` - check slot
- `start_new_day()` - new day
- `get_day_info()` - formatted info
- `advance_days(n)` - skip days
- `is_morning()`, `is_afternoon()`, `is_evening()`, `is_night()` - convenience checks

**Dependencies:** state.rpy (for current_day, time_slot)
**Called by:** All story files
**Rollback/save:** Time progression must be deterministic.

---

### 8. 00_systems/college_manager.rpy
**Responsibility:** Education tracking, classes, assignments, library
**State owned:**
- Uses `education_progress`, `has_college_id`, `college_course` from state.rpy
- `assignments_due`, `classes_attended`, `library_visits` (local defaults)

**Public functions:**
- `get_education_progress()` - current progress
- `add_education_progress(amount)` - add progress
- `attend_class()` - attend class session
- `study_at_library(hours)` - study session
- `complete_assignment(name)` - complete assignment
- `add_assignment(name, due_day)` - add assignment
- `get_upcoming_assignments()` - list assignments
- `has_completed_enough_credits()` - milestone check

**Dependencies:** state.rpy (for education_progress, etc.)
**Called by:** Story files (college scenes)
**Rollback/save:** Progress changes must be explicit.

---

### 9. 00_systems/employment_manager.rpy
**Responsibility:** Job management, shifts, wages
**State owned:**
- Uses `employment_state`, `current_job`, `shift_today`, `work_experience` from state.rpy
- `starter_job` dict, `shifts_worked`, `workplace_hours` (local defaults)

**Public functions:**
- `get_job_info()` - current job
- `start_job(job_definition)` - start employment
- `end_job()` - end employment
- `work_shift()` - complete shift (pays wages)
- `get_earnings()` - shift earnings
- `is_employed()` - employment check
- `get_workplace_name()` - workplace name
- `get_job_description()` - job description

**Dependencies:** state.rpy (for employment_state, current_job, money)
**Called by:** Story files (work scenes), location files
**Rollback/save:** Wage payment must happen exactly once per shift.

---

### 10. 00_systems/event_manager.rpy
**Responsibility:** Event tracking, recent events, day summaries
**State owned:**
- Uses `recent_events`, `day_summary` from state.rpy

**Public functions:**
- `record_event(event_type, character_id, details)` - log event
- `get_recent_events(limit)` - recent events
- `has_event_type(event_type)` - event check
- `get_events_for_character(character_id)` - character events
- `record_day_summary(summary_dict)` - day summary
- `get_day_summary(day)` - get summary
- `clear_recent_events()` - clear events

**Dependencies:** state.rpy (for recent_events, day_summary)
**Called by:** All story files, location files
**Rollback/save:** Event logs should be deterministic.

---

## Initialization Order

Ren'Py loads files in alphabetical order by default. Current order:

1. `characters/generated_encounters.rpy` - uses character_registry
2. `characters/protagonist.rpy` - defines protagonist, p Character
3. `characters/recurring_cast.rpy` - registers authored characters
4. `locations/*/location_*.rpy` - uses location_manager, state
5. `screens/*/*.rpy` - screen definitions
6. `screens.rpy` - main screens
7. `script.rpy` - entry point, initializes state
8. `40_story/prologue/*.rpy` - story content
9. `40_story/chapter*.rpy` - legacy chapters
10. `systems/*.rpy` - system modules
11. `world_map/world_map.rpy` - location data

**Issue:** Systems are loaded AFTER story files. Story files reference system functions that don't exist yet.

**Fix needed:** Systems should load BEFORE story files. Use `init offset` or rename files to ensure proper order.

---

## Rollback/Save Safety Summary

| Module | Save-safe? | Notes |
|--------|------------|-------|
| state.rpy | YES | Uses `default` for all playthrough vars |
| character_registry.rpy | MOSTLY | used_names set should be rollback-safe |
| relationship_manager.rpy | YES | Values in character dicts, if state is default |
| encounter_manager.rpy | CRITICAL | Random ID generation must be stable |
| location_manager.rpy | YES | Uses defaults from state |
| economy_manager.rpy | YES | Money uses default |
| time_manager.rpy | YES | Day/slot use default |
| college_manager.rpy | YES | Progress uses default |
| employment_manager.rpy | YES | Job state uses default |
| event_manager.rpy | YES | Events list - verify list is rollback-safe |

---

## Known Issues

1. **Load order:** Systems load after story files - may cause "undefined" errors
2. **used_names set:** Python set may not be rollback-safe - needs verification
3. **character dicts:** Should verify they use Ren'Py defaults not Python dicts
4. **generated_characters:** Random character creation must be deterministic after save/load
