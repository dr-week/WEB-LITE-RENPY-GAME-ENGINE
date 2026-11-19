# Save/Load/Rollback Test Report

**Date:** 2026-11-13
**Ren'Py Version:** NOT TESTED (SDK not accessible)
**Status:** BLOCKED - Requires Ren'Py Launcher

## Test Scope

Per v0.6 Phase 3, Task 4, the following scenarios need testing:

1. Save before generating a character
2. Generate a new encounter
3. Save after the encounter
4. Load the saved game
5. Verify the same character ID, name and relationship data
6. Roll back before the encounter
7. Replay the encounter
8. Roll back across a money transaction
9. Verify no duplicated charges or wages
10. Verify time and energy are restored correctly

## System Design Review (Static Analysis)

### Character Identity Preservation

**Design:** Characters stored in `recurring_characters` and `generated_characters` dictionaries with stable IDs.

**Rollback Safety Assessment:**
- **CONCERN:** Python dictionaries and sets may not participate in Ren'Py rollback correctly
- **DESIGN REQUIREMENT:** All playthrough state should use `default` declarations, not Python objects
- **STATUS:** Needs Ren'Py testing to verify

### Money Transaction Safety

**Design:** Money is a `default` variable in state.rpy, modified by `add_money()` and `spend_money()` functions.

**Rollback Safety Assessment:**
- **GOOD:** Money uses `default` - should be rollback-safe
- **CONCERN:** Function calls that modify money must be deterministic
- **STATUS:** Needs Ren'Py testing to verify no double-charging

### Time Progression Safety

**Design:** `current_day` and `time_slot` are `default` variables.

**Rollback Safety Assessment:**
- **GOOD:** Uses `default` - should be rollback-safe
- **STATUS:** Needs Ren'Py testing to verify

### Encounter Generation Safety

**Design:** `generate_encounter_character()` creates random ID and name, stores in `generated_characters`.

**Rollback Safety Assessment:**
- **CRITICAL CONCERN:** Random ID generation must be stable across save/load
- **CONCERN:** If random seed changes between sessions, could generate different character
- **STATUS:** Needs Ren'Py testing to verify

## State Variables and Rollback Safety

| Variable | Declaration | Rollback-Safe? | Notes |
|----------|-------------|----------------|-------|
| money | default | YES | Standard Ren'Py default |
| current_day | default | YES | Standard Ren'Py default |
| time_slot | default | YES | Standard Ren'Py default |
| energy | default | YES | Standard Ren'Py default |
| recurring_characters | default dict | UNCERTAIN | Dict may not rollback correctly |
| generated_characters | default dict | UNCERTAIN | Dict may not rollback correctly |
| used_names | default set | UNCERTAIN | Python set NOT rollback-safe |
| story_flags | default dict | UNCERTAIN | Dict may not rollback correctly |
| recent_events | default list | UNCERTAIN | List may not rollback correctly |

## Critical Concerns

1. **used_names set** - Python sets are NOT rollback-safe. Names could regenerate after rollback.
2. **Character dictionaries** - May not persist correctly across rollback
3. **Random encounter IDs** - Must verify deterministic behavior

## Required Testing

1. **Character persistence test:**
   - Start new game
   - Meet an encounter character
   - Save game
   - Load game
   - Verify same character ID and name appear
   - Verify relationship values preserved

2. **Rollback test:**
   - Advance through dialogue
   - Rollback to before encounter
   - Verify character is not created yet
   - Replay encounter
   - Verify same character created (same ID)

3. **Money transaction test:**
   - Spend money
   - Save
   - Load
   - Verify money balance correct
   - Rollback after spending
   - Verify money restored

## Conclusion

Cannot complete testing without Ren'Py SDK. Static analysis reveals potential rollback safety issues with Python data structures (dicts, sets) that need verification.

## Next Steps

1. Access Ren'Py SDK
2. Run character persistence test
3. Run rollback test
4. Run money transaction test
5. Fix any rollback issues found
