# Dungeon Keep — Session State

## Design Pivot v2 (2026-09-25)
**Source:** `game-direction-v2.md` — New core fantasy: *"Build a living dungeon. Recruit monsters. Set up defenses. Then watch adventurers invade and try to survive your dungeon."*

**Key shift:** Strip guild/crafting/trading from MVP. Focus entirely on **dungeon layout + room synergies + auto-combat**. The dungeon itself is the character.

---

## Current Milestone
**M2: Room-Based Defense (Dungeon Maker Core)** — IN PROGRESS 🔄

---

## Progress
- [x] **M1:** Skeleton (Architecture & Rendering) — COMPLETE
- [x] **M2 Core:** Entrance tile, linear hero path, stationary monsters, traps on walk-over
- [x] **Grid resize:** 6×4 with 72px tiles (big room blocks)
- [x] **Balance:** Hero speeds 0.5/0.4/0.3 tiles/s, 8s prep phase before wave 1
- [x] **Bug fix:** Heroes can walk through rooms (pathfinding no longer blocked by Lair/Trap/Treasury)
- [x] **Bug fix:** A* fallback uses Manhattan-stepped path
- [x] `game-direction-v2.md` written — full design direction for MVP

---

## What's Working Now
1. `python main.py`
2. Title screen → click to start → 8s prep countdown ("Prep: Xs")
3. **6×4 grid of large 72px tiles**
4. Build Lair / Trap / Treasury on big room blocks
5. Click Lair → recruit Goblin / Slime / Skeleton
6. Heroes spawn at brown ENTRANCE (left edge) and march toward Dungeon Core (right edge)
7. Monsters are **stationary** — they fight heroes who enter their tile
8. Traps trigger when hero **walks ON** the trap tile
9. Heroes deal damage to Dungeon Core (100 HP) when they reach it
10. Win/loss screens, Enter to restart

---

## What Makes It Boring Right Now
- **No player agency during combat** — just watch
- **No room synergies** — a Slime in a Trap tile is the same as a Slime anywhere
- **No monster abilities** — just HP/damage/attack speed
- **Auto-start waves** — player can't choose when ready
- **No progression between waves** — monsters auto-heal, no loot, no upgrades
- **Heroes are generic** — no party composition, no roles

---

## v2 MVP Scope (from `game-direction-v2.md`)

### Monsters (3 types)
| Monster | Role | Ability |
|---------|------|---------|
| 🟢 Slime | Tank / Slow | Slows enemies in same room |
| 👺 Goblin | Basic DPS | Attacks quickly |
| ☠️ Skeleton | Durable DPS | Revives once at 50% HP |

### Heroes (3 types)
| Hero | Role | Ability |
|------|------|---------|
| 🛡️ Knight | Tank | High HP |
| 🏹 Archer | Ranged | Attacks from distance |
| 🧙 Mage | AoE | Damages multiple monsters |

### Rooms (6 types)
| Room | Function |
|------|----------|
| Spike Trap | Damages first hero entering |
| Slime Pool | Slimes here slow enemies by 50% |
| Goblin Den | Goblins here attack 2× faster |
| Skeleton Crypt | Skeletons here revive once at 50% HP |
| Treasure Room | (passive gold?) |
| Dungeon Core | If destroyed, game over |

### Core Loop
```
BUILD → RECRUIT → ARRANGE → START INVASION → AUTO COMBAT → LOOT → UPGRADE → REPEAT
```

### Waves (5 total)
1. Knight
2. Knight + Archer
3. Knight + Archer + Mage
4. 2 Knights + Archer
5. Full party

### One Emergency Ability
🔮 **Dark Magic** — Click an enemy → deal 30 damage, 10s cooldown

---

## Open Decisions (Pending User Input)

### 1. Grid Size
- **A.** Keep 6×4 — tight, tactical
- **B.** Widen to 8×4 or 10×4 — longer gauntlet, more combos

### 2. Monsters Per Room
- **A.** 1 monster per tile (current)
- **B.** Each tile is a "room" holding 1–3 monsters

### 3. Between Waves
- **A.** Instant — auto-heal, gold awarded, "Next Wave" button appears
- **B.** Relaxed — player clicks "Next Invasion" when ready

### 4. Strip or Hide Old Code
- **A.** Strip guild/crafting/trading code now (cleaner)
- **B.** Hide them (comment out) — keep for later

### 5. Room Count for First Playable
- **A.** All 6 room types at once
- **B.** Start with fewer (Trap + 3 monster rooms), add rest later

---

## Recently Completed
- `game-direction-v2.md` — full v2 design direction
- Grid resize to 6×4 with 72px tiles
- Hero speed balance + prep phase
- Pathfinding bug fixes

## Blockers
- None.

## Session Handoff Notes
- All code committed and pushed to `https://github.com/ta-brook/dungeon-keep`
- To resume: clone repo, `pip install -r requirements.txt`, `python main.py`
- Design docs: `DESIGN_VISION.md` (original hybrid), `game-direction-v2.md` (stripped MVP)
- `SPEC.md` contains old milestone structure — needs updating for v2

## Next Steps (when resuming)
1. Get user answers to **5 Open Decisions** above
2. Update `SPEC.md` with v2 MVP milestones
3. Implement v2 MVP core:
   - Manual "Defend" button (replace auto-start)
   - Room synergies (Slime slow, Goblin fast, Skeleton revive)
   - Dark Magic emergency ability
   - 5 waves with party composition
   - Post-invasion loot + upgrade loop
4. Smoke test for fun

## Date: 2026-09-25
## Session: Design pivot v2 + M2 core implementation + v2 planning
