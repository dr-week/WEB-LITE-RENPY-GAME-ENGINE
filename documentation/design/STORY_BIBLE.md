# Story bible

## Core concept

A choice-driven life story about building an independent routine in a new city:
college, first work, friendships, money decisions, and personal wellbeing.
Choices change skills, relationships, resources, and which later scenes appear.

## Protagonist and setting

- Current protagonist: Maya, 19, she/her. Core profile defaults live in `game/10_characters/protagonist.rpy` and reset via `init_new_game_state()`.
- Recurring cast introduced across Week 1 (`00_systems/core/state_init.rpy`): **Elena** (classmate), **Marcus** (cafe coworker), and **Priya** (study partner).
- Current starting balance: 120 dollars (provisional value alongside optional fictional BTC portfolio).
- Current opening places: home, bus stop, college/classroom, library, cafe (`The Daily Grind Cafe`), park, and city streets.
- The city and country remain unnamed until a setting note is approved.

## Narrative Flow & Choice Design Rules

- **Guided Days 1–7 Arc (`day_router.rpy`)**:
  - **Day 1**: Morning pressure -> bus commute -> campus classroom & Elena -> afternoon class/library -> evening cafe interview & first shift (`40_story/prologue/`).
  - **Days 2–6**: Daily morning chapter beat -> 3-pillar afternoon/evening hub (`day_hub.rpy`) for **Study**, **Work**, or **Lifestyle / City Journal (`image_story_hub.rpy`)** -> night wrap (`end_day_home` -> `end_day`).
  - **Day 7 & Beyond**: `week_01_evaluation` (`40_story/endings/week_01_eval.rpy`) evaluates academic, financial, intelligence, and appeal growth into four outcomes (`thriving`, `academic`, `independent`, `finding_footing`), then opens open-ended Week 2 routine (`day_free_morning.rpy`).
- **Rule of 2–3 Meaningful Choices**: Every story and location menu offers 2–3 focused options (never bloated 6–8 item lists).
- **Consequential Choices**: Every choice modifies at least one tangible state — **Money / BTC**, **Intelligence / Learning**, **Appeal / Confidence**, **Work Skill / Communication / Financial Literacy**, **Wellbeing (Energy / Stress / Health)**, or **Relationships** — with no dead `pass` branches.
- Do not make a single stat or money shortage permanently block progression; keep free ($0) alternatives alongside paid choices.

## Visual rule: no character sprites

No on-screen character sprites, pose layers, or sprite-expression switching. Use
dialogue names and text for speakers, location backgrounds for setting, and
optional full-frame CG illustrations for story moments. Reference images are
generation inputs only and are never displayed as character sprites.
