# LOLA Narration Audit Report

Generated from `developer-tools/checks/narration_auditor.py` across `game/40_story/` and `game/20_locations/`.

---

## 1. Problems Found

### A. Maya Spoken Lines Over 6 Words (`long_maya_line`)
| File & Line | Words | Current Text | Recommended Short Gen-Z Line |
| --- | --- | --- | --- |
| `game/40_story/chapters/day_02_class.rpy:14` | 11 | `"You're a lifesaver. Seriously, slept right through two alarms—brain's still mush."` | `"Lifesaver. Slept through two alarms."` |
| `game/40_story/chapters/day_02_class.rpy:32` | 11 | `"Rain check—lemme lock these three thesis hooks down before they evaporate."` | `"Rain check. Locking thesis notes."` |
| `game/40_story/chapters/day_03_pressure.rpy:10` | 10 | `"{cps=26}Ugh... $[money] left till Friday. C'mon, Maya, figure it out...{/cps}"` | `"{cps=26}Ugh... $[money] left. Figure it out.{/cps}"` |
| `game/40_story/chapters/day_03_pressure.rpy:18` | 12 | `"Two days of real food for six bucks. Boring? Yeah. Smart? Definitely."` | `"Six bucks, two days. Smart."` |
| `game/40_story/chapters/day_03_pressure.rpy:23` | 7 | `"Zero dollars spent. Stomach's complainin', wallet's smilin'."` | `"Zero spent. Wallet's happy."` |
| `game/40_story/chapters/day_04_connection.rpy:34` | 11 | `"{cps=30}S'fine, lemme clear my head outside—I'll send my half in twenty.{/cps}"` | `"{cps=30}Need air. Sending my half soon.{/cps}"` |
| `game/40_story/chapters/day_05_deadline.rpy:16` | 10 | `"Hey, pressure makes diamonds—or at least decent footnotes. Watch this."` | `"Pressure makes diamonds. Watch this."` |
| `game/40_story/chapters/day_05_deadline.rpy:38` | 9 | `"{cps=24}Whew... barely made the bell. Brain's totally fried, m'kay.{/cps}"` | `"{cps=24}Barely made it. Brain's fried.{/cps}"` |

### B. Dry Placeholder Narration & Verbal Tics (`dry_or_tic_narration`)
| File & Line | Issue | Current Text | Recommended Fix |
| --- | --- | --- | --- |
| `game/40_story/chapters/day_hub.rpy:6` | `"m'kay"` tic + mixed POV | `"Maya's eyelids drooped—'m'kay... zero battery left, gotta crash.'"` | Split into narration + `maya_thought "Zero battery. Gotta crash."` |
| `game/40_story/chapters/day_free_morning.rpy:9` | Dry header | `"Day [current_day] - Morning"` | `"Day [current_day] — pale morning light across the room."` |
| `game/40_story/prologue/day_02_home.rpy:11` | Dry header | `"Day [current_day] - Morning"` | `"Day [current_day] — city hums awake outside."` |
| `game/40_story/prologue/day_01_work_search.rpy:75` | Dry placeholder | `"Shift over. She had earned some money."` | `"Shift over. Tips clinked in her pocket—worth the hustle."` |
| `game/40_story/prologue/day_end.rpy:8` | Dry placeholder | `"Home again."` | `"Lock clicked shut behind her—safe, tired, home."` |
| `game/40_story/prologue/day_end.rpy:9` | Dry placeholder | `"Day [current_day] complete."` | `"Another day in Solis Bay tucked away."` |

---

## 2. How to Re-Run the Audit

```bash
python developer-tools/checks/narration_auditor.py --json
```
