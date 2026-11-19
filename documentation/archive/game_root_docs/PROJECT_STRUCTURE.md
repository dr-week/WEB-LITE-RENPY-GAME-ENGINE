# LOLA - Visual Novel Project Structure

## Overview
LOLA is a modular Ren'Py visual novel featuring a college student's first experiences in a new city. The game includes:
- Daily gameplay loop system
- Multiple romance paths
- Dynamic outfit switching
- Relationship tracking
- Random name generation
- Location-based activities
- **Love scene system with progressive unlocking**

## Project Structure

```
game/
├── script.rpy              # Main game entry point and configuration
├── gui.rpy                 # GUI configuration (unchanged)
├── options.rpy             # Game options (unchanged)
├── screens.rpy             # Screen definitions (unchanged)
│
├── modular/               # All game systems organized by function
│   │
│   ├── characters/
│   │   └── main_character.rpy
│   │       - MainCharacter class with stats (money, energy, reputation)
│   │       - Methods for outfit/expression management
│   │       - protagonist instance initialization
│   │
│   ├── outfits/
│   │   └── outfit_system.rpy
│   │       - OutfitSystem class
│   │       - ConditionSwitch for dynamic sprite rendering
│   │       - Supports 3 outfits x 2 expressions (6 sprites)
│   │
│   ├── relationships/
│   │   ├── relationship_system.rpy
│   │   │   - Relationship class (trust, attraction, rivalry)
│   │   │   - RelationshipSystem class managing all 3 romance paths
│   │   │   - Affection level calculations
│   │   │
│   │   └── love_scenes.rpy
│   │       - LoveSceneSystem class
│   │       - 7 scenes per romance path (21 total)
│   │       - Attraction-based scene unlocking
│   │       - Threshold management
│   │
│   ├── random/
│   │   └── random_name_generator.rpy
│   │       - RandomNameGenerator class
│   │       - 10 male names, 10 female names
│   │       - Deterministic random generation using renpy.random.choice()
│   │
│   ├── locations/
│   │   ├── home.rpy       # Apartment (outfit changing, resting)
│   │   ├── school.rpy     # Education hub (classes, socializing, studying)
│   │   ├── cafe.rpy       # Work & social (shifts, encounters, drinks)
│   │   ├── club.rpy       # Nightlife (dancing, flirting, partying)
│   │   └── jungle.rpy     # Adventure area (hiking, romance, meditation)
│   │
│   └── story/
│       ├── chapter1.rpy
│       │   - Game introduction and setup
│       │   - Protagonist arrival in new city
│       │   - Romance path selection
│       │   - Initial stat establishment
│       │
│       ├── daily_loop.rpy
│       │   - DailyLoop class managing game progression
│       │   - Periods: morning, school, afternoon, evening, night, sleep
│       │   - Period advancement and day cycling
│       │   - 30% chance of love scene at night
│       │
│       ├── love_events.rpy
│       │   - Love scene labels (21 total)
│       │   - Attraction-based dialogue
│       │   - Stat updates per scene
│       │   - Integration with relationship system
│       │
│       └── endings.rpy
│           - Multiple endings based on relationship routes
│           - Affection-level dependent ending variations
│           - Stranger, School Boyfriend, City Bully endings
│           - Neutral/Self-Discovery ending
│
├── images/
│   ├── sprites/               # Character sprite images (to be added)
│   │   ├── kurta_normal.png
│   │   ├── kurta_flirty.png
│   │   ├── skirt_normal.png
│   │   ├── skirt_flirty.png
│   │   ├── bikini_normal.png
│   │   └── bikini_flirty.png
│   │
│   └── love/                  # Love scene images (to be added)
│       ├── stranger/
│       │   ├── hand_hold.png
│       │   ├── hug_scene.png
│       │   ├── kiss_scene.png
│       │   ├── night_walk.png
│       │   ├── bed_scene1.png
│       │   ├── bed_scene2.png
│       │   └── bed_scene3.png
│       │
│       ├── school_bf/
│       │   ├── hand_hold.png
│       │   ├── hug_scene.png
│       │   ├── kiss_scene.png
│       │   ├── movie_night.png
│       │   ├── bed_scene1.png
│       │   ├── bed_scene2.png
│       │   └── bed_scene3.png
│       │
│       └── bully/
│           ├── hand_hold.png
│           ├── hug_scene.png
│           ├── kiss_scene.png
│           ├── club_dance.png
│           ├── bed_scene1.png
│           ├── bed_scene2.png
│           └── bed_scene3.png
│
├── backgrounds/           # Location backgrounds (to be added)
│   ├── home.jpg
│   ├── school.jpg
│   ├── jungle.jpg
│   ├── cafe.jpg
│   └── club.jpg
```

## Game Systems

### Character System (modular/characters/main_character.rpy)
The `protagonist` object tracks:
- `money` (starts at 500)
- `energy` (0-100 scale)
- `reputation` (social standing)
- `current_outfit` (kurta, skirt, bikini)
- `current_expression` (normal, flirty)

Methods:
- `add_money(amount)` - Adjust finances
- `rest()` - Restore energy to 100
- `change_outfit(outfit, expression)` - Switch appearance
- `get_sprite()` - Return current sprite name

### Outfit System (modular/outfits/outfit_system.rpy)
Uses Ren'Py's `ConditionSwitch` to dynamically display sprites based on protagonist properties.
The `player` image automatically updates when outfit or expression changes.

**Sprite Combinations:**
- Kurta + Normal
- Kurta + Flirty
- Skirt + Normal
- Skirt + Flirty
- Bikini + Normal
- Bikini + Flirty

### Relationship System (modular/relationships/relationship_system.rpy)
Three romance paths with independent tracking:

**Stranger Route**
- Random name generated at game start
- met through chance encounters
- Attraction-focused relationship

**School Boyfriend Route**
- Pre-established past relationship
- named "Alex"
- Nostalgia and rekindling focus

**City Bully Route**
- Antagonistic character
- named "Jordan"
- Tension and rivalry dynamics

Each relationship has:
- `trust` (0-100)
- `attraction` (0-100)
- `rivalry` (0-100)
- `get_score()` - Combined metric
- `get_affection_level()` - Returns: hostile, indifferent, interested, close, intimate

### Random Name Generator (modular/random/random_name_generator.rpy)
Male names: Arjun, Kabir, Rohan, Dev, Neel, Aryan, Aditya, Vikram, Samrat, Akshar
Female names: Priya, Ananya, Diya, Riya, Simran, Nisha, Isha, Kavya, Adira, Zara

Deterministic random generation ensures same name on replays.

### Daily Loop System (modular/story/daily_loop.rpy)
`DailyLoop` class manages game progression:
- Periods: morning → school → afternoon → evening → night → sleep
- Auto-increments to next day after sleep
- Day counter displayed to player

**Daily Cycle:**
1. **Morning** - Wake up, check stats, choose activities
2. **School** - Attend classes, socialize, study
3. **Afternoon** - Work shift at cafe, earn money
4. **Evening** - Social activities (cafe, school, jungle, club)
5. **Night** - Special events, romantic encounters
6. **Sleep** - Day wraps up, next day begins

### Location System

**Home** - Safe space
- Change outfits
- Rest and restore energy
- Check status
- Safe zone

**School** - Education
- Attend classes (+reputation, -energy)
- Socialize (+reputation, -energy, +relationships)
- Study (+reputation)

**Cafe** - Work & Social
- Work shift (+money, -energy, +reputation)
- Meet encounters (+attraction)
- Buy drinks (-money)

**Club** - Nightlife
- Dance (-energy)
- Flirt (-energy, +attraction, changes expression to flirty)
- Party hard (-energy, -money, +reputation)

**Jungle** - Adventure
- Hike (+reputation, -energy)
- Secret Meeting (+attraction, change to flirty expression)
- Meditate (+energy)

### Story Progression (modular/story/)

**Chapter 1** (chapter1.rpy)
- Arrival in new city
- Apartment setup
- First day impressions
- Romance path selection menu
- Initial stat setup

**Daily Loop** (daily_loop.rpy)
- Implements full game loop
- Period transitions
- Status displays
- Navigation menus
- Continuation/ending options

**Endings** (endings.rpy)
Multiple endings based on highest relationship score:
- **Stranger Route**: True Love, Romantic, or Bittersweet
- **School Boyfriend Route**: Second Chance, Closure, or Moving On
- **City Bully Route**: Dangerous Love, Obsession, or Unresolved Tension
- **Neutral Route**: Self-Discovery (if no clear dominant relationship)

Each ending has 3 variations based on affection level.

## Variable Tracking

### Protagonist Stats
```python
protagonist.money          # 0-infinity (starts 500)
protagonist.energy         # 0-100
protagonist.reputation     # 0-infinity
protagonist.current_outfit # "kurta", "skirt", "bikini"
protagonist.current_expression # "normal", "flirty"
```

### Relationship Stats (per romance path)
```python
relationship.trust         # 0-100
relationship.attraction    # 0-100
relationship.rivalry       # 0-100
```

### Game Progress
```python
daily_loop.current_day     # 1, 2, 3, ...
daily_loop.current_period  # "morning", "school", "afternoon", etc.
```

## How to Add Content

### Add New Sprites
1. Place PNG files in `sprites/` folder
2. Update `image player = ConditionSwitch(...)` in `outfit_system.rpy`
3. Add conditions for new outfit/expression combinations

### Add New Locations
1. Create `locations/LOCATION_NAME.rpy`
2. Define `label LOCATION_NAME:` for entry point
3. Add location to navigation menus in daily_loop
4. Define background image

### Add New Relationship
1. Update `relationship_system.rpy` to add new character type
2. Add name generation if random (update `random_name_generator.rpy`)
3. Create ending scenario in `endings.rpy`
4. Add to romance selection menu in `chapter1.rpy`

### Add New Activities
1. Create label for activity in relevant location file
2. Modify stats appropriately
3. Add menu option to location

## File Dependencies

Files are loaded in order by Ren'Py:
1. Main script.rpy
2. gui.rpy, options.rpy, screens.rpy
3. modular/characters/main_character.rpy
4. modular/outfits/outfit_system.rpy
5. modular/relationships/relationship_system.rpy
6. modular/random/random_name_generator.rpy
7. modular/locations/*.rpy
8. modular/story/*.rpy

## Running the Game

1. Ensure all image placeholder files exist in sprites/ and backgrounds/
2. Run Ren'Py and select the game folder
3. Click "Launch Project"
4. Start game from main menu

## Default Placeholders

Background images are currently solid colors:
- bg_home: Brown (#8B7355)
- bg_school: Sky Blue (#87CEEB)
- bg_jungle: Forest Green (#228B22)
- bg_cafe: Brown (#D2691E)
- bg_club: Dark Slate Gray (#2F4F4F)

Replace with actual image files for production build.

## Tips for Expansion

1. **More sprites**: Add new outfits by expanding outfit_system.rpy conditions
2. **More locations**: Each location is self-contained in one file
3. **More characters**: Relationship system easily supports additional romance paths
4. **Story branches**: Add conditions in chapter1.rpy and daily_loop.rpy
5. **Mini-games**: Create new labels and call from location labels
6. **Sound effects**: Add `play sound "audio/soundname.ogg"` to activity labels
