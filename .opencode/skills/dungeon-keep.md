# Dungeon Keep — Project Skill

## Overview
Dungeon Keep is a **real-time-with-pause** 2D pixel-art dungeon management and guild simulation game.
- **Genre:** Dungeon-building / defense / guild management / crafting / raiding hybrid
- **Tech:** Python + Pygame, compiled to browser via Pygbag
- **Scope:** 8 milestones — M1–M4 core dungeon defense, M5–M8 guild management expansion
- **Vibe:** Dark / gritty fantasy dungeon + guild management
- **Inspiration:** Creator Chronicles (guild management sim) meets Dungeon Keeper (dungeon defense)

## Team Structure

| Role | Responsibilities |
|------|------------------|
| **PM** | Milestone planning (M1–M8), scope gatekeeping, acceptance criteria, economy balance review |
| **Senior Developer** | Architecture, core systems, code review, performance, integration |
| **Designer** | Pixel art sprites, tilesets, UI mockups, color palette, animation specs, NPC portraits |
| **Economy Systems Designer** | Crafting recipes, trade balance, profession rates, raid difficulty, NPC progression |

## Tech Stack & Environment

- **Engine:** Pygame 2.5+
- **Browser Build:** Pygbag (`pygbag .` from project root)
- **Python:** 3.10+
- **Screen Size (M1–M4):** 512 x 384 logical pixels (16x12 grid of 32px tiles)
- **Screen Size (M5+):** 768 x 384 logical pixels (24x18 grid, camera scrolling)
- **Scale:** 2x for browser display (1024 x 768 → 1536 x 768)

## Coding Conventions

- **Style:** PEP 8, 4-space indentation, max line length 100
- **Imports:** `import pygame` first, then stdlib, then project modules
- **Naming:** `snake_case` for functions/variables/files, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- **Types:** Use type hints on all public functions and class methods
- **Docstrings:** Google-style docstrings for all modules, classes, and public methods
- **State Management:** Single `GameState` enum/class; no global mutable state
- **Rendering:** All draw calls go through a centralized `renderer.py`; entities expose `.draw(surface, camera)` methods
- **Events:** Use Pygame event queue; no blocking input loops
- **Asset Loading:** Load once at startup in `assets.py`; use dictionary lookups, not filesystem reads per frame

## Architecture Rules

1. **Separation of Concerns:**
   - `entities.py` — data and behavior only, no drawing logic
   - `renderer.py` — all blitting and sprite rendering
   - `ui.py` — buttons, panels, text (drawn via `renderer.py`)
   - `grid.py` — tile map, pathfinding, collision data
   - `combat.py` — damage formulas, attack cooldowns, death resolution
   - `npc.py` — NPC data, guild management, morale system
   - `professions.py` — profession definitions, production ticks, leveling
   - `crafting.py` — recipes, resource inventory, crafting queue
   - `raids.py` — raid party formation, auto-battle, loot tables
   - `trading.py` — auction house, market demand, visitors
   - `village.py` — multi-tile building placement, grid expansion
   - `codex.py` — progression tracking, completion %, milestone rewards
   - `chronicle.py` — event log, timestamps, summary generation
   - `camera.py` — camera system for scrolling (M5+)

2. **No Circular Imports:** `constants.py` and `assets.py` are leaf modules. `main.py` is the root.

3. **Game Loop (fixed timestep):**
   ```
   Process Input -> Update Logic (if not paused) -> Render Frame
   ```
   Target: 60 FPS. Use `dt` (delta time in seconds) for all movement, cooldowns, and production ticks.

4. **Entity Component Pattern (lightweight):**
   - Base `Entity` class with `update(dt)`, `draw(surface, camera_offset)`
   - `Monster(Entity)`, `Hero(Entity)`, `Projectile(Entity)`
   - Composition for behaviors: `CombatStats`, `Movement` as mixin/dataclass attributes
   - `NPC` is a separate dataclass (not an Entity) — managed by `GuildManager`

5. **Pathfinding:**
   - M1–M4: A* on the 16x12 grid. Grid nodes are walkable or blocked by rooms/monsters. Heroes recalculate path every 0.5 seconds.
   - M5+: A* on the 24x18 grid with camera scrolling. Buildings block tiles.

6. **Economy Systems (M5+):**
   - All production/crafting/raid systems use `dt` for frame-rate independence
   - Economy balance is tuned by `dungeon-economy` agent, reviewed by PM at milestone gates
   - No infinite gold exploits — all income sources are bounded
   - Raid auto-battle is deterministic (same inputs = same outputs)

## Asset Pipeline

- **Format:** PNG with transparency
- **Sprite Size:** 32x32 base, scaled 2x at render time
- **Palette:** Restricted dark fantasy palette (defined in `assets/palette.png` or constants)
- **Naming:** `tiles_stone_floor.png`, `unit_goblin.png`, `ui_panel.png`, etc.
- **Animation:** Sprite sheets horizontal; frame count in filename or constants

## Build & Run Commands

```bash
# Run locally
python main.py

# Build for browser
pygbag .

# The output is in build/web/; serve with any static server
python -m http.server 8000 --directory build/web
```

## Module Interface Contracts

### `grid.py`
```python
class Grid:
    def __init__(self, width: int, height: int) -> None: ...
    def is_walkable(self, x: int, y: int) -> bool: ...
    def set_tile(self, x: int, y: int, tile_type: TileType) -> None: ...
    def get_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]: ...
```

### `entities.py`
```python
class Entity(ABC):
    def update(self, dt: float, grid: Grid) -> None: ...
    def take_damage(self, amount: int) -> None: ...
    @property
    def is_alive(self) -> bool: ...
```

### `combat.py`
```python
def resolve_attack(attacker: Entity, target: Entity, dt: float) -> None: ...
def find_target(entity: Entity, enemies: List[Entity], range_tiles: int) -> Optional[Entity]: ...
```

### `ui.py`
```python
class Button:
    def __init__(self, rect: pygame.Rect, text: str, callback: Callable) -> None: ...
    def handle_event(self, event: pygame.event.Event) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
```

## Milestones (PM-Defined)

| Milestone | Acceptance Criteria | Role Lead |
|-----------|---------------------|-----------|
| M1: Skeleton | Grid renders, click detection, placeholder rects, camera works | Senior Dev |
| M2: Build & Economy | Place rooms, spend gold, UI panel, Treasury income | Senior Dev |
| M3: Units & Combat | Recruit monsters, hero spawning, basic combat, death | Senior Dev + Designer |
| M4: Waves & Polish | 3 waves, pause/resume, win/lose screens, all art in | Designer + Senior Dev |
| M5: NPC & Guild | NPC recruitment, guild panel, personalities, morale | Senior Dev + Designer |
| M6: Crafting & Professions | Multi-tile buildings, profession production, crafting queue, 15+ recipes | Senior Dev + Economy |
| M7: Dungeon Raids | Raid party formation, auto-battle, loot, soft permadeath | Senior Dev + Economy |
| M8: Trading, Codex & Chronicle | Auction house, market demand, codex completion, event chronicle | Senior Dev + Economy + Designer |

## Communication Protocol

- **Designer → Senior Dev:** Deliver sprites as PNGs in `assets/`; provide animation frame counts and pivot points in `assets/manifest.json`
- **Senior Dev → Designer:** Provide screen dimensions, grid specs, and color constants before M1; provide panel layouts for M5+ UI
- **Economy → Senior Dev:** Deliver balance tables (recipes, loot, production rates) as data dicts; review at M6, M7, M8 gates
- **PM → All:** Define milestone scope; reject feature creep; approve spec changes via PR to `SPEC.md`; review economy balance at M6 gate

## Interaction Rules

- **Always ask in interactive mode:** When clarifying requirements, making design choices, or requesting user decisions, use the interactive `question` tool with multiple-choice options. Do not ask open-ended text questions unless no choices can be provided.
- **Always commit and push:** After every meaningful change (feature completion, bug fix, milestone boundary, or session end), commit with a descriptive message and push to the remote repository immediately. Never leave unpushed commits at the end of a session.

## Constraints & Non-Goals

- **NO** multiplayer or networking
- **NO** saving/loading (prototype only — session state only)
- **NO** complex AI (heroes use A* toward Dungeon Heart; monsters use simple aggro radius; raids use deterministic auto-battle)
- **NO** audio for M1–M3; optional SFX in M4 if time permits
- **NO** scrolling camera in M1–M4 (single screen only); camera added in M5
- **NO** more than 3 dungeons, 12 guild members, or 30 NPC portraits in prototype scope
- **NO** economy balance changes without `dungeon-economy` agent or PM approval
