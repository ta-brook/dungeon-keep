# Dungeon Keep Prototype — Project Skill

## Overview
Dungeon Keep is a **real-time-with-pause** 2D pixel-art dungeon management prototype.
- **Genre:** Dungeon-building / defense / tycoon hybrid
- **Tech:** Python + Pygame, compiled to browser via Pygbag
- **Scope:** Single-screen prototype, 3 waves, win/lose condition
- **Vibe:** Dark / gritty fantasy

## Team Structure

| Role | Responsibilities |
|------|------------------|
| **PM** | Milestone planning, scope gatekeeping, acceptance criteria, prioritization |
| **Senior Developer** | Architecture, core systems, code review, performance, integration |
| **Designer** | Pixel art sprites, tilesets, UI mockups, color palette, animation specs |

## Tech Stack & Environment

- **Engine:** Pygame 2.5+
- **Browser Build:** Pygbag (`pygbag .` from project root)
- **Python:** 3.10+
- **Screen Size:** 512 x 384 logical pixels (16x12 grid of 32px tiles)
- **Scale:** 2x for browser display (1024 x 768 canvas)

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

2. **No Circular Imports:** `constants.py` and `assets.py` are leaf modules. `main.py` is the root.

3. **Game Loop (fixed timestep):**
   ```
   Process Input -> Update Logic (if not paused) -> Render Frame
   ```
   Target: 60 FPS. Use `dt` (delta time in seconds) for all movement and cooldowns.

4. **Entity Component Pattern (lightweight):**
   - Base `Entity` class with `update(dt)`, `draw(surface, camera_offset)`
   - `Monster(Entity)`, `Hero(Entity)`, `Projectile(Entity)`
   - Composition for behaviors: `CombatStats`, `Movement` as mixin/dataclass attributes

5. **Pathfinding:**
   - Prototype uses A* on the 16x12 grid.
   - Grid nodes are walkable or blocked by rooms/monsters.
   - Heroes recalculate path every 0.5 seconds or on obstacle change.

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

## Communication Protocol

- **Designer → Senior Dev:** Deliver sprites as PNGs in `assets/`; provide animation frame counts and pivot points in `assets/manifest.json`
- **Senior Dev → Designer:** Provide screen dimensions, grid specs, and color constants before M1
- **PM → All:** Define milestone scope; reject feature creep; approve spec changes via PR to `SPEC.md`

## Interaction Rules

- **Always ask in interactive mode:** When clarifying requirements, making design choices, or requesting user decisions, use the interactive `question` tool with multiple-choice options. Do not ask open-ended text questions unless no choices can be provided.

## Constraints & Non-Goals

- **NO** multiplayer or networking
- **NO** saving/loading (prototype only)
- **NO** complex AI (heroes use A* toward Dungeon Heart; monsters use simple aggro radius)
- **NO** audio for M1–M3; optional SFX in M4 if time permits
- **NO** scrolling camera (single screen only)
