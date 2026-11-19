# Love Scene System - Complete Implementation Guide

## Overview

The Love Scene System provides dynamic, romance-path-specific content that progresses as player attraction increases. Each romance path has unique dialogue and scenes that unlock at specific attraction thresholds.

---

## System Architecture

### Components

1. **Love Scene Class** (`modular/relationships/love_scenes.rpy`)
   - `LoveSceneSystem` - Manages unlocking and progression
   - Tracks attraction thresholds for each scene
   - Maintains unlocked scenes per character

2. **Love Events** (`modular/story/love_events.rpy`)
   - Scene labels for each romance path
   - Attraction-triggered dialogue
   - Integration with relationship system

3. **Image Folders** (`images/love/`)
   - `stranger/` - Stranger romance scenes
   - `school_bf/` - School boyfriend scenes
   - `bully/` - City bully scenes

4. **Daily Loop Integration** (`modular/story/daily_loop.rpy`)
   - 30% chance of love scene trigger at night (after day 3)
   - Automatic progression based on attraction

---

## Scene Progression System

### Stranger Romance Path

| Scene | Attraction Threshold | Title | Image |
|-------|----------------------|-------|-------|
| hand_hold | 15+ | Hand Hold | love/stranger/hand_hold.png |
| hug_scene | 35+ | A Warm Embrace | love/stranger/hug_scene.png |
| kiss_scene | 55+ | First Kiss | love/stranger/kiss_scene.png |
| night_walk | 70+ | Night Walk | love/stranger/night_walk.png |
| bed_scene1 | 80+ | Intimate Moment | love/stranger/bed_scene1.png |
| bed_scene2 | 90+ | Passion | love/stranger/bed_scene2.png |
| bed_scene3 | 100 | Complete Union | love/stranger/bed_scene3.png |

### School Boyfriend Romance Path

| Scene | Attraction Threshold | Title | Image |
|-------|----------------------|-------|-------|
| hand_hold | 15+ | Reconnection | love/school_bf/hand_hold.png |
| hug_scene | 35+ | Familiar Comfort | love/school_bf/hug_scene.png |
| kiss_scene | 55+ | Rekindling | love/school_bf/kiss_scene.png |
| movie_night | 70+ | Movie Night | love/school_bf/movie_night.png |
| bed_scene1 | 80+ | Nostalgia | love/school_bf/bed_scene1.png |
| bed_scene2 | 90+ | Remember Us | love/school_bf/bed_scene2.png |
| bed_scene3 | 100 | Forever | love/school_bf/bed_scene3.png |

### City Bully Romance Path

| Scene | Attraction Threshold | Title | Image |
|-------|----------------------|-------|-------|
| hand_hold | 15+ | Unexpected Touch | love/bully/hand_hold.png |
| hug_scene | 35+ | Dangerous Embrace | love/bully/hug_scene.png |
| kiss_scene | 55+ | Power Play | love/bully/kiss_scene.png |
| club_dance | 70+ | Club Chemistry | love/bully/club_dance.png |
| bed_scene1 | 80+ | Tension | love/bully/bed_scene1.png |
| bed_scene2 | 90+ | Surrender | love/bully/bed_scene2.png |
| bed_scene3 | 100 | Obsession | love/bully/bed_scene3.png |

---

## How Love Scenes Trigger

### Automatic Triggering

1. **Night Events** (30% chance at night after day 3)
   - `label night_love_encounter` checks all romance relationships
   - Finds character with highest attraction
   - Checks if new scene unlocks
   - Displays scene if unlocked

2. **Attraction Updates**
   - Each scene adds to attraction when completed
   - Stranger scenes: +5 to +20 attraction points
   - School BF scenes: +6 to +18 attraction points
   - Bully scenes: +5 to +20 attraction points

3. **Trust & Rivalry**
   - Different paths affect different stats
   - Bully path: Rivalry decreases as scenes progress
   - Stranger/School BF: Trust increases with scenes

### Manual Triggering

Scenes can be manually called in dialogue:

```renpy
label my_custom_event:
    call love_scene_stranger_kiss_scene
```

---

## File Structure

```
game/
├── images/
│   └── love/
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
└── modular/
    ├── relationships/
    │   ├── relationship_system.rpy
    │   └── love_scenes.rpy           [NEW]
    │
    └── story/
        ├── daily_loop.rpy            [MODIFIED]
        └── love_events.rpy           [NEW]
```

---

## Code Integration

### Love Scene System Class

```python
love_scenes = LoveSceneSystem()

# Get path to image
image_path = love_scenes.get_scene_image_path("stranger", "kiss_scene")
# Returns: "love/stranger/kiss_scene"

# Check if new scene unlocks
new_scene = love_scenes.check_scene_unlock("stranger", 65)
# Returns: {"name": "night_walk", "threshold": 70, "title": "Night Walk"}
# or None if no new scene unlocks
```

### Love Event Triggering

```python
# Night event with 30% chance
$ love_encounter = renpy.random.randint(1, 100) > 70

if love_encounter and daily_loop.current_day > 3:
    call night_love_encounter
```

### Manual Scene Display

```renpy
label custom_scene:
    show expression love_scenes.get_scene_image_path("stranger", "kiss_scene")
    "Dialogue here"
```

---

## Creating New Love Scenes

### Step 1: Add Image File
Place image in appropriate folder:
- `images/love/stranger/my_scene.png`
- `images/love/school_bf/my_scene.png`
- `images/love/bully/my_scene.png`

### Step 2: Add to Scene List
Edit `modular/relationships/love_scenes.rpy`:

```python
LOVE_SCENES = {
    "stranger": [
        # ...existing scenes...
        {"name": "my_scene", "threshold": 75, "title": "My Scene Title"}
    ]
}
```

### Step 3: Create Scene Label
Add to `modular/story/love_events.rpy`:

```renpy
label love_scene_stranger_my_scene:
    scene black with fade
    show expression love_scenes.get_scene_image_path("stranger", "my_scene") with dissolve
    
    "Your dialogue here"
    
    $ relationship_sys.get_relationship("stranger").add_attraction(10)
    $ relationship_sys.get_relationship("stranger").add_trust(5)
    
    with fade
    scene black
    return
```

### Step 4: Test
Play game and reach the attraction threshold to trigger the scene.

---

## Customization Examples

### Change Attraction Threshold

In `modular/relationships/love_scenes.rpy`:

```python
{"name": "kiss_scene", "threshold": 50, "title": "First Kiss"}  # Was 55
```

### Add Stat Changes

In `modular/story/love_events.rpy`:

```renpy
label love_scene_stranger_kiss_scene:
    # ...existing code...
    $ protagonist.add_money(100)        # Add money reward
    $ protagonist.add_reputation(20)    # Add reputation
    $ daily_loop.current_day += 1       # Skip a day
```

### Add Conditional Scenes

```renpy
label night_love_encounter:
    # ...existing code...
    
    if protagonist.current_outfit == "bikini":
        "They're particularly attracted to you tonight..."
        $ relationship_sys.get_relationship(romance_type).add_attraction(15)
    else:
        $ relationship_sys.get_relationship(romance_type).add_attraction(10)
```

---

## Dialogue Variables

Scene labels have access to:

```python
romance_type          # "stranger", "school_bf", "bully"
romance_rel           # Relationship object
highest_attraction    # Attraction value of chosen character
new_scene             # New scene that just unlocked
```

And global variables:

```python
protagonist           # Main character object
daily_loop           # Daily loop manager
relationship_sys     # Relationship system
love_scenes          # Love scene system
```

---

## Art Requirements

Each romance path needs 7 images:

1. **hand_hold.png** - Tender moment of holding hands
2. **hug_scene.png** - Warm embrace
3. **kiss_scene.png** - First kiss
4. **[path-specific].png** - Unique scene per path
   - Stranger: night_walk
   - School BF: movie_night
   - Bully: club_dance
5. **bed_scene1.png** - Initial intimate moment
6. **bed_scene2.png** - Intense moment
7. **bed_scene3.png** - Climactic moment

**Total images needed: 21** (7 per path × 3 paths)

**Recommended resolution:** 1920x1080 (HD)

---

## Testing Love Scenes

### Debug Method

Add to any location to test scenes instantly:

```renpy
label test_love_scenes:
    $ relationship_sys.get_relationship("stranger").attraction = 65
    $ relationship_sys.get_relationship("school_bf").attraction = 75
    $ relationship_sys.get_relationship("city_bully").attraction = 85
    
    call night_love_encounter
```

### Progression Testing

1. Start game
2. Play normally and increase attraction through activities
3. After day 3, each night has 30% chance of love scene
4. Check attraction levels to verify progression

---

## Performance Notes

- Images loaded on-demand during scenes
- No preloading - keeps memory usage low
- Scenes fade to black for smooth transitions
- Compatible with all Ren'Py versions

---

## Troubleshooting

**Image not showing:**
- Verify file exists in correct folder
- Check filename matches exactly (case-sensitive on Linux/Mac)
- Confirm image format is supported (PNG, JPG recommended)

**Scene not triggering:**
- Ensure attraction is high enough
- Check daily_loop.current_day > 3
- Verify 30% random chance triggered
- Check that relationship exists

**Wrong character's scene displays:**
- Verify romance_type variable is set correctly
- Check relationship scores to ensure highest is correct
- Debug with print statements

**Image path errors:**
- Verify love_scenes.get_scene_image_path() returns correct string
- Check Ren'Py image directory is correct
- Ensure images/ folder contains love/ subfolder

---

## API Reference

### LoveSceneSystem Methods

```python
get_available_scenes(character_type)
    # Returns list of all scenes for character
    # Args: "stranger", "school_bf", "bully"
    # Returns: [{"name": "...", "threshold": X, "title": "..."}, ...]

check_scene_unlock(character_type, attraction_level)
    # Check if new scene unlocks at this attraction level
    # Args: character_type (str), attraction_level (int)
    # Returns: scene dict or None

get_scene_image_path(character_type, scene_name)
    # Get image path for rendering
    # Args: character_type (str), scene_name (str)
    # Returns: "love/character_type/scene_name"
```

### Attraction Threshold Ranges

```
0-14    → No scenes available
15-34   → hand_hold available
35-54   → hug_scene available
55-69   → kiss_scene available
70-79   → path-specific scene available
80-89   → bed_scene1 available
90-99   → bed_scene2 available
100     → bed_scene3 available
```

---

## Future Expansion Ideas

- Branching dialogue based on previous scenes
- Relationship-specific customization options
- Multiple dialogue options in love scenes
- Stat rewards for completed scenes
- Unlock endings based on love scene progression
- NPC reactions to relationship status
- Photo gallery of viewed scenes
- Love scene achievement system
