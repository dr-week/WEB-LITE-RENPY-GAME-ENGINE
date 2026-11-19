# Blocking Issues Report

**Date:** 2026-11-13
**Phase:** 3 - Ren'Py Validation

## Critical Blockers

### B-001: Ren'Py SDK Not Accessible
- **Severity:** CRITICAL
- **Description:** Cannot run Ren'Py lint, launch game, or perform gameplay testing
- **Impact:** All Phase 3 testing blocked
- **Status:** OPEN
- **Workaround:** None - requires Ren'Py SDK access
- **Resolution needed:** User must provide Ren'Py SDK access or run tests manually

## Potential Issues Requiring Ren'Py Testing

### P-001: Python Data Structure Rollback Safety
- **Severity:** HIGH
- **Description:** `used_names` is a Python set, which may not be rollback-safe
- **Impact:** Character names could regenerate after rollback
- **Status:** NOT TESTED
- **Location:** `00_systems/state.rpy`

### P-002: Character Dictionary Rollback
- **Severity:** HIGH
- **Description:** `recurring_characters` and `generated_characters` are Python dicts
- **Impact:** Character data may not persist correctly across rollback
- **Status:** NOT TESTED
- **Location:** `00_systems/state.rpy`

### P-003: Init Order Conflicts
- **Severity:** MEDIUM
- **Description:** Ren'Py init priorities may override directory numbering
- **Impact:** Systems may not load in correct order
- **Status:** NOT TESTED
- **Location:** All system files

### P-004: Variable Initialization Order
- **Severity:** MEDIUM
- **Description:** Some story files may reference variables before initialization
- **Impact:** "Undefined variable" errors at runtime
- **Status:** NOT TESTED

## Already Fixed (Not Blocking)

### F-001: Nested game/game/ directory
- **Status:** FIXED - Removed

### F-002: Duplicate location_travel labels
- **Status:** FIXED - Renamed to unique names

### F-003: Duplicate arrive_college label
- **Status:** FIXED - Renamed to arrive_college_transport

### F-004: Duplicate cafe_job_interview label
- **Status:** FIXED - Renamed to cafe_job_interview_location

### F-005: Duplicate screen world_map()
- **Status:** FIXED - Removed duplicate

### F-006: Legacy modular/ inside game/
- **Status:** FIXED - Moved to legacy_archive/

### F-007: Legacy chapter files in game/
- **Status:** FIXED - Moved to legacy_archive/story_legacy/

### F-008: Orphaned .rpyc files
- **Status:** FIXED - Removed

## Verification Status Summary

| Check | Status |
|-------|--------|
| No nested game/game/ | PASS |
| 35 .rpy files | PASS |
| Legacy outside game/ | PASS |
| No duplicate labels | PASS (static) |
| No duplicate screens | PASS (static) |
| Renamed labels have correct callers | PASS (static) |
| Ren'Py lint | BLOCKED |
| Game launch | BLOCKED |
| Vertical slice gameplay | BLOCKED |
| Save/load/rollback | BLOCKED |
| Visual QA | BLOCKED |

## Resolution Requirements

To proceed past Phase 3, the following is required:

1. **Access to Ren'Py SDK** - Either:
   - Install Ren'Py in accessible location, OR
   - Run tests from machine with Ren'Py installed, OR
   - Provide SDK path for automated testing

2. **After SDK access:**
   - Run lint and fix errors
   - Launch game and test vertical slice
   - Test save/load/rollback
   - Verify visual presentation

## Current Recommendation

The architecture and namespace issues are resolved. Static analysis shows no duplicate labels, screens, or structural problems. The project is ready for Ren'Py testing - the only blocker is SDK access.

Suggested user action: Open Ren'Py Launcher on this project and run Check Script (Lint), then report results.
