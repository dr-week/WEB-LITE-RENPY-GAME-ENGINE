# LOLA Visual Novel - Implementation Plan
# Based on Master Planning v0.3 and Implementation Replan v0.4

## Current Status: Phase 0-1 in Progress

### What Exists
- `game/` directory with new architecture structure
- `game/script.rpy` - Core game script with systems
- `game/gui.rpy` - Custom GUI configuration
- `game/screens.rpy` - Custom screens including world map
- `game/options.rpy` - Options and configuration
- `game/world_map/world_map.rpy` - World map system
- `game/characters/characters.rpy` - Character definitions (placeholder)
- `game/story/prologue.rpy` - First playable vertical slice (NEW)
- `game/systems/game_state.rpy` - Game state system (NEW)
- `game/systems/encounter_manager.rpy` - Encounter system (NEW)
- `game/systems/location_manager.rpy` - Location system (NEW)
- `images/` - 277+ image files (not yet reviewed)
- `developer-tools/pixel-anime-converter/` - Asset converter tool

### Phase 0: Repository Audit (IN PROGRESS)

**Completed:**
- Verified project structure
- Confirmed `game/` directory exists with new architecture
- Located image assets in `images/` directory
- Read existing game files

**Still Needed:**
- [ ] Full recursive image inventory
- [ ] Contact sheets for visual review
- [ ] Verify `love/` folder contents
- [ ] Identify truncated filenames

### Phase 1: Minimal Game Foundation

**Completed:**
- [x] Created `game_state.rpy` with core state variables
- [x] Created `encounter_manager.rpy` with two-layer character system
- [x] Created `location_manager.rpy` with location definitions
- [x] Created `prologue.rpy` with first playable vertical slice
- [x] Updated `script.rpy` to use new systems
- [x] Updated `options.rpy` with proper defaults

**Still Needed:**
- [ ] Verify Ren'Py launches the project
- [ ] Test the vertical slice flows correctly
- [ ] Fix any broken references or missing labels

### Phase 2: First Playable Vertical Slice

**Scope (from Replan v0.4):**
1. Protagonist at home with financial problem
2. Commute decision (bus stop)
3. First college scene
4. One encounter (classmate)
5. Job search/first work scene
6. Day-wrap/status update
7. Save/load/rollback functional

**Completed:**
- [x] Home scene with financial pressure
- [x] Bus stop travel scene
- [x] College arrival and classroom
- [x] Classmate encounter with choices
- [x] Library study option
- [x] Cafe job interview scene
- [x] First work shift with choices
- [x] Day wrap and continue

**Still Needed:**
- [ ] Test all menu choices lead to valid destinations
- [ ] Test save/load/rollback during slice
- [ ] No soft-locks or broken flows

### Phase 3: Light Life State

**Completed:**
- [x] `money` with clear income/cost
- [x] `day` and `time_slot` progression
- [x] `energy` (optional but useful)
- [x] `education_progress` (milestone-based)
- [x] `employment_state` (one starter job)
- [x] `story_flags` for key events

**Still Needed:**
- [ ] Test money transactions apply once
- [ ] Test rollback doesn't duplicate transactions
- [ ] No grind or soft-lock

### Phase 4: Character Identity (Partial)

**Completed:**
- [x] Two-layer character system (authored + generated)
- [x] Stable character IDs
- [x] Name generation once at encounter creation
- [x] Per-character friendship/romance/hostility
- [x] Used-name registry

**Still Needed:**
- [ ] Test generated names don't change on reload
- [ ] Test screen redraw doesn't create characters
- [ ] Visual assets for characters (pending image review)

### What NOT to Build Yet (from Replan v0.4)

**Explicitly Deferred:**
- [ ] Complex dashboard or UI polish
- [ ] Account/login systems
- [ ] Cloud asset management
- [ ] Real-time collaboration
- [ ] Multiple simultaneous jobs
- [ ] Full open-world schedule
- [ ] Dozens of life meters
- [ ] Fixed romance-route/ending quotas
- [ ] Runtime image conversion

### Known Unknowns (from Replan v0.4)

These should be confirmed with the user before finalizing:
- [ ] Protagonist's exact name (currently "Maya" as provisional)
- [ ] Country/city setting
- [ ] Currency type
- [ ] College course
- [ ] Exact age (must be 18+)
- [ ] Family/background details
- [ ] Living arrangement
- [ ] Starter job (need visual review of work images)

### Immediate Next Steps

1. **Test the vertical slice** - Launch Ren'Py and verify the prologue flows
2. **Fix any broken references** - Check for missing labels, images, or variables
3. **Create REPOSITORY_AUDIT.md** - Document current state
4. **Review key images** - Select a few for vertical slice testing
5. **Get user confirmation** on protagonist details before expanding

---

## File Manifest

### Game Files (Primary)
```
game/
├── script.rpy                    # Main script with lifecycle
├── options.rpy                   # Configuration and defaults
├── gui.rpy                       # GUI styling
├── screens.rpy                   # Custom screens
├── characters/
│   └── characters.rpy           # Character definitions (placeholder)
├── story/
│   ├── prologue.rpy             # First vertical slice
│   ├── chapter1.rpy             # (Legacy - may be replaced)
│   ├── chapter2.rpy             # (Legacy - may be replaced)
│   ├── chapter3.rpy             # (Legacy - may be replaced)
│   └── chapter4_endings.rpy     # (Legacy - may be replaced)
├── systems/
│   ├── game_state.rpy           # Core state management
│   ├── encounter_manager.rpy    # Character encounters
│   └── location_manager.rpy     # Locations and travel
├── world_map/
│   └── world_map.rpy           # World map navigation
├── assets/                      # (empty - for processed assets)
├── audio/                       # (empty - for audio files)
└── developer-tools/             # Secondary tools
    └── pixel-anime-converter/   # Asset converter
```

### Notes
- Legacy chapter files (chapter1-4) may need to be replaced with new story structure
- Prologue.rpy is the new starting point for the vertical slice
- Systems are designed to be modular and Ren'Py-native
- No custom engine - using Ren'Py's built-in features
