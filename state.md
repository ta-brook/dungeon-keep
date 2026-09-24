# Dungeon Keep — Session State

## Current Milestone
**M3: Units & Combat** — In Progress

## Progress
- [x] Project scaffold created
- [x] SPEC.md written
- [x] Agents configured
- [x] Skill configured
- [x] Git repository initialized, committed, pushed
- [x] **TICKET-001: Design Deliverables** — COMPLETE
- [x] **TICKET-002: M1 Skeleton Implementation** — COMPLETE
- [x] **TICKET-003: M2 Build & Economy** — COMPLETE
- [x] **TICKET-004: M3 Units & Combat** — IN PROGRESS

## Open Tickets

### TICKET-004: M3 Units & Combat
**Status:** In Progress  
**Assignee:** Senior Dev  
**Description:** Implement monsters, heroes, combat system, pathfinding, wave spawning, recruitment, and win/loss conditions.  
**Affected Files:**
- `constants.py` — monster/hero stats
- `grid.py` — A* pathfinding
- `entities.py` — Entity base, Monster, Hero with stats
- `combat.py` — damage, targeting, cooldowns, trap damage
- `waves.py` — wave definitions, spawn timers
- `build_system.py` — recruitment from Lairs
- `ui.py` — recruit menu when clicking Lair
- `renderer.py` — draw entities, HP bars
- `main.py` — game logic loop, spawning, combat, death, win/loss
**Acceptance Criteria:**
- [ ] Clicking a Lair opens recruit menu
- [ ] Recruiting spawns monster at Lair location
- [ ] Heroes spawn at map edge and move toward Dungeon Heart
- [ ] Heroes path around walls and rooms (A*)
- [ ] Monsters aggro heroes within 3 tiles
- [ ] Combat deals damage based on stats
- [ ] Death removes entity and awards gold (heroes only)
- [ ] All stats use `dt` for frame-rate independence
- [ ] 3 waves spawn progressively
- [ ] Dungeon Heart destroyed = Loss
- [ ] All waves cleared + no heroes = Win

## Recently Completed
- M2 Build & Economy: rooms, gold, build feedback

## Blockers
None.

## Next Steps
1. Implement all M3 systems
2. Test combat and wave flow
3. Commit and push
