# LOLA - Visual Novel

A choice-driven life-story visual novel built with Ren'Py.

## Project Structure

```
LOLA/
├── game/                    # Ren'Py project directory (runtime)
│   ├── script.rpy          # Entry point
│   ├── options.rpy         # Configuration
│   ├── gui.rpy            # GUI styling
│   ├── screens.rpy        # Screen declarations
│   ├── characters/        # Character definitions
│   ├── story/             # Narrative content
│   ├── systems/           # Game systems
│   ├── locations/         # Location data
│   ├── screens/           # Custom screens
│   ├── data/              # Static data
│   ├── images/            # Runtime images (organized)
│   ├── audio/             # Audio files
│   └── tl/                # Translations
│
├── developer-tools/        # NOT imported by game
│   └── pixel-anime-converter/
│
├── tests/
├── documentation/
├── tools/
└── README.md
```

## Development Status

- Version: 0.1.0 (vertical slice in progress)
- Target: Ren'Py 8.6.0

## Quick Start

1. Install Ren'Py 8.6.0
2. Open `game/` as a Ren'Py project
3. Run the game

## Documentation

See `documentation/` for architecture, audits, and decisions.
