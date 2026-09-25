# Dungeon Keep — Player Manual

> **Version:** M4 (Build, Recruit, Defend Core Loop)  
> **Last Updated:** 2026-09-25

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## Controls

| Input | Action |
|-------|--------|
| **Left Click** | Select tile, build room, recruit monster, or interact with UI |
| **Spacebar** | Toggle pause |
| **ESC** | Cancel build / cancel recruit / unpause |
| **Enter** | Restart game (on Win / Loss screen) |

---

## Game Flow

1. **Title Screen** — Click anywhere to start.
2. **Game Screen** — Build rooms, recruit monsters, and defend your Dungeon Heart.
3. **Win / Loss** — Press **Enter** to restart.

---

## Objective

Defend your **Dungeon Heart** from waves of invading heroes. Survive all 3 waves to win. If a hero reaches the Dungeon Heart, you lose.

---

## Sidebar (Build & Recruit)

On the right side of the screen:

- **Gold Counter** — Your current gold. Treasuries generate +1 gold/second each.
- **Build Buttons:**
  - **Lair** (50g) — Required to recruit monsters. Click a placed Lair to open the recruit menu.
  - **Trap Room** (40g) — Damages heroes on adjacent floor tiles.
  - **Treasury** (60g) — Passively generates gold.
- Click a build button, then click an empty floor tile to place it.

### Recruiting Monsters

1. Build a **Lair**.
2. **Left-click the Lair** on the map.
3. Choose a monster:
   - **Goblin** (20g) — Fast, fragile
   - **Slime** (15g) — Slow, tanky
   - **Skeleton** (30g) — High damage

---

## Combat

- **Monsters** automatically attack heroes that enter their aggro radius (3 tiles).
- **Heroes** pathfind toward the Dungeon Heart and attack anything in their way.
- **Trap Rooms** deal damage to heroes standing on adjacent floor tiles.
- Killing a hero awards **+10 gold**.

---

## Pause System

Press **Spacebar** to pause. While paused:
- ✅ You **can** build rooms
- ✅ You **can** recruit monsters
- ❌ Traps do not damage heroes
- ❌ Heroes and monsters do not move or attack

Press **Spacebar** again to resume.

---

## Waves

| Wave | Enemies | Notes |
|------|---------|-------|
| 1 | 3 Adventurers | Basic heroes |
| 2 | 4 Adventurers + 2 Knights | Knights are slower but tougher |
| 3 | 5 Adventurers + 3 Knights + 1 Paladin | Paladin is very strong |

A short delay between waves gives you time to build and recruit.

---

## Tips

- Build **Treasuries** early for passive income.
- Place **Trap Rooms** near chokepoints or the Dungeon Heart.
- **Slimes** are cheap tanks; **Skeletons** deal heavy damage.
- You can build and recruit while paused — use the downtime between waves!

---

## Known Issues / In Progress

- No sound effects yet.
- No save/load (session-only).
- Post-M4 content (guild system, crafting, raids, trading) is planned for future milestones.
