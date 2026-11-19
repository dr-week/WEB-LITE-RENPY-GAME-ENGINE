# Solis Bay — Symmetrical 3x3 Structured Map Blueprint & Prompt Script

## 1. Why a 3x3 Symmetrical Sector Grid (`3840x2160`)

Asymmetric maps waste corners, crowd buildings unpredictably, and make pin placement fragile. Dividing the 16:9 canvas into **9 equal `1280x720` sectors** separated by two straight horizontal avenues (`y=720`, `y=1440`) and two straight vertical avenues/canal (`x=1280`, `x=2560`) guarantees zero wasted space and exact, symmetrical pin placement:

| Row \ Col | Col 1: West (`x: 0–1280`, `cx=640`) | Col 2: Center (`x: 1280–2560`, `cx=1920`) | Col 3: East (`x: 2560–3840`, `cx=3200`) |
| --- | --- | --- | --- |
| **Row 1: North (`y: 0–720`, `cy=360`)** | **[1,1] Pinecrest Ridge & Viewpoint** | **[1,2] Observation Tower Plaza** | **[1,3] University & School Campus** |
| **Row 2: Mid (`y: 720–1440`, `cy=1080`)** | **[2,1] Apartments (`home`) & Bus/Rail Hub** | **[2,2] Market Street & Cafe Plaza** | **[2,3] College Library & Study Commons** |
| **Row 3: South (`y: 1440–2160`, `cy=1800`)** | **[3,1] Old Dockside Tenements (Slum)** | **[3,2] Solis Harbor & Waterfront Piers** | **[3,3] Botanical Gardens & Emerald Park** |

---

## 2. Structured 3x3 Curved Radial-Ring Prompt Script (`[FIELD: {...}; (...)]` Syntax)

Combines the exact zero-waste 3x3 sector symmetry with **graceful concentric ring-roads, curved boulevards, circular plazas, and rounded district blocks**:

```text
[ASSET_ID: ui_map_solis_bay_curved_grid_v1]
[SCENE: LOLA interactive city map, 16:9 widescreen 4K — Solis Bay symmetrical curved radial-ring city]
[CAMERA: {Strict 90-degree top-down orthographic overhead view with subtle elevation depth-of-field}; (ZERO sky, ZERO horizon line, ZERO oblique tilt)]
[STRUCTURE: {Symmetrical radial-ring and curved-boulevard urban plan anchored by a grand central circular plaza, concentric sweeping ring-roads, rounded corner blocks, and a gently curving central canal}; (balanced 3x3 zone symmetry with zero wasted corners and organic architectural curvature)]
[STYLE: {Hybrid aesthetic illustration combining clean contemporary anime architecture with semi-realistic environmental textures, soft neutral daylight, and refined matte-painted foliage}; (minimum visual clutter, smooth curved avenues, crisp uncluttered rooftops, muted-realistic urban palette)]
[ROW_1_NORTH: {TOP-LEFT: terraced green mountain ridge with a curved stone cliffside viewpoint overlook}; {TOP-CENTER: grand circular stone roundabout anchored by a tall landmark observation clock tower}; {TOP-RIGHT: curved university campus quad with symmetrical school halls and an oval sports track}]
[ROW_2_MIDDLE: {MID-LEFT: curved brick apartment crescent with round courtyard on left and a semi-circular bus-and-rail transit hub on right}; {CENTER: circular pedestrian market plaza with curved shopfronts and a distinct corner cafe terrace}; {MID-RIGHT: circular glass-domed college library surrounded by curved study paths and lawns}]
[ROW_3_SOUTH: {BOTTOM-LEFT: dense weathered low-income tenement slum blocks curving along the rail bend}; {BOTTOM-CENTER: semi-circular coastal harbor bay basin with curved waterfront promenade and radiating wooden piers}; {BOTTOM-RIGHT: manicured botanical gardens with concentric circular flowerbeds, curved glass conservatory, and round park pond}]
[FRAME: {Full-bleed 16:9 edge-to-edge structured cartography engineered for exact pin placement at the center of each of the 9 curved zones}; (even neutral daylight ready for day-to-night tinting)]
[AVOID: rigid boxy 90-degree grid monotony, asymmetric messy sprawl, pixel art, 16-bit RPG tiles, noisy miniature toy clutter, sky, horizon line, text, street labels, map pins, UI icons, people, vehicles crowding roads, watermark]
```
