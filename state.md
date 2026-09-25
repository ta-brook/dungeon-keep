# Dungeon Keep — Session State

## Design Pivot
**2026-09-25** — Project pivoted to Evil Hunter Tycoon × Dungeon Maker × Creator Chronicles hybrid. See `DESIGN_VISION.md` for full vision. `SPEC.md` updated with new milestones.

---

## Current Milestone
**M2: Room-Based Defense (Dungeon Maker Core)** — IN PROGRESS 🔄

## Progress
- [x] **M1:** Skeleton (Architecture & Rendering) — COMPLETE
- [x] **M2 Pre-work:** Button scaling fix, restart on win/loss, trap damage fix, discrete hero movement
- [x] **M2 Design:** `DESIGN_VISION.md` written, `SPEC.md` milestones updated
- [x] **TICKET-009:** Entrance tile added (left edge), heroes spawn at Entrance and path to Heart
- [x] **TICKET-010:** Monster AI refactored — stationary in rooms, only attack heroes in same tile
- [x] **TICKET-011:** Traps refactored — trigger when hero walks ON trap tile (not adjacent)
- [x] **TICKET-012:** Renderer updated for Entrance tile, trap indicators moved to trap tile, heart HP bar added
- [x] Dungeon Heart HP system added (100 HP, heroes deal damage when on heart tile)

## Open Tickets
- **TICKET-013:** Smoke test M2 — run game, verify heroes walk Entrance→Heart, monsters defend rooms, traps trigger on walk-over, heart takes damage
- **TICKET-014:** Balance pass — monster/hero stats, trap damage, heart HP, wave difficulty

## Recently Completed
- Fixed UI button scaling (SCALE_FACTOR bug in `ui.py`)
- Added restart on Enter key for win/loss screens
- Fixed trap damage (fractional accumulation)
- Changed hero movement to discrete tile steps
- Fixed hero teleport bug (A* to unwalkable Dungeon Heart + safety clamp)
- Wrote `DESIGN_VISION.md` and updated `SPEC.md`
- **M2 Implementation:**
  - `constants.py`: Added `ENTRANCE` TileType + color
  - `grid.py`: `_place_entrance()` on left edge, `find_entrance()`, `is_walkable` includes ENTRANCE
  - `waves.py`: Heroes spawn at `find_entrance()` instead of random edges
  - `entities.py`: `Monster.update()` stripped of movement — monsters are now stationary
  - `combat.py`: Monster/hero combat range reduced to 0.5 (same tile only); trap damage triggers on hero.grid_x == trap_x and hero.grid_y == trap_y
  - `main.py`: Added `dungeon_heart_hp` tracking (100 max), heroes damage heart when on tile
  - `renderer.py`: Draws ENTRANCE tile, trap indicators on trap tiles, heart HP bar above heart

## Blockers
- None.

## Session Handoff Notes
- All code committed and pushed
- To resume: clone repo, `pip install -r requirements.txt`, `python main.py`
- New design doc: `DESIGN_VISION.md`
- Updated spec: `SPEC.md` Section 10

## What You Can Play Now (M2 Core)
1. `python main.py`
2. Title screen → click to start
3. Build Lair / Trap / Treasury on grid
4. Click Lair → recruit Goblin / Slime / Skeleton (monster spawns IN the Lair, stationary)
5. Heroes spawn at brown ENTRANCE tile (left edge) and march tile-by-tile toward Dungeon Heart
6. When a hero enters a tile with a monster, combat begins (both attack each other)
7. When a hero walks ON a Trap tile, they take 5 DPS
8. If heroes reach the Dungeon Heart, they damage it (100 HP total)
9. Win/loss screens with Enter to restart
10. **Monsters no longer chase** — they only fight in their assigned room

## Next Steps
1. **TICKET-013:** Smoke test M2 gameplay
2. **TICKET-014:** Balance pass
3. **M3:** Day/Night cycle

## Date: 2026-09-25
## Session: M2 Implementation — Room-Based Defense Core
