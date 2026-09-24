# Dungeon Keep Prototype — Specification

## 1. Game Concept

**Dungeon Keep** is a real-time-with-pause dungeon management defense prototype. The player builds rooms, recruits monsters, and defends their Dungeon Heart against waves of invading heroes.

- **Perspective:** Top-down 2D grid
- **Theme:** Dark fantasy dungeon
- **Core Loop:** Build → Recruit → Defend → Earn Gold → Expand

## 2. Screen Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Title Screen│────▶│ Game Screen │────▶│ Win / Loss  │
└─────────────┘     └─────────────┘     └─────────────┘
                          ▲                   │
                          └───────────────────┘
```

### 2.1 Title Screen
- Dark stone background
- Game title centered
- "Start Prototype" button
- Brief instruction text

### 2.2 Game Screen
- Main play area: 512x384 (left/top)
- UI sidebar: 256x384 (right) — build buttons, gold, wave info, pause button
- Total logical resolution: **768x384** (scaled 2x to 1536x768 in browser)

### 2.3 Win / Loss Screen
- Overlay on game screen
- Win: "Dungeon Secured!" + stats (waves survived, gold earned)
- Loss: "Dungeon Heart Destroyed!" + stats
- "Restart" button

## 3. Core Mechanics

### 3.1 Grid System
- **Dimensions:** 16 tiles wide × 12 tiles tall
- **Tile Size:** 32 × 32 pixels
- **Coordinate System:** Grid coordinates `(gx, gy)` where `0 <= gx < 16`, `0 <= gy < 12`
- **Pixel Mapping:** `px = gx * 32`, `py = gy * 32`

### 3.2 Tile Types

| Tile Type | Walkable | Buildable | Description |
|-----------|----------|-----------|-------------|
| `STONE_WALL` | No | No | Impassable dungeon boundary |
| `STONE_FLOOR` | Yes | Yes | Default empty floor |
| `DUNGEON_HEART` | No | No | Core building; heroes target this; if destroyed, game over |
| `LAIR` | No | No | Spawns monsters; click to recruit |
| `TRAP_ROOM` | No | No | Damages heroes walking on adjacent floor tiles |
| `TREASURY` | No | No | Passively generates +1 gold per second |

### 3.3 Economy

- **Starting Gold:** 150
- **Costs:**
  - Lair: 50 gold
  - Trap Room: 40 gold
  - Treasury: 60 gold
  - Goblin: 20 gold
  - Slime: 15 gold
  - Skeleton: 30 gold
- **Income:**
  - Treasury: +1 gold/sec per Treasury
  - Hero kill: +10 gold

### 3.4 Rooms

- Rooms occupy **1 tile** (32x32) for prototype simplicity.
- Building requires clicking an empty `STONE_FLOOR` tile and selecting a room type from the UI.
- Only **Senior Dev** may change room size to multi-tile in future specs; PM must approve.

### 3.5 Monsters

| Monster | HP | Damage | Attack Speed | Move Speed | Cost | Special |
|---------|----|--------|--------------|------------|------|---------|
| Goblin | 30 | 5 | 1.0/s | 2.0 tiles/s | 20 | Fast, fragile |
| Slime | 50 | 3 | 0.8/s | 1.0 tiles/s | 15 | Slow, tanky |
| Skeleton | 40 | 8 | 0.6/s | 1.5 tiles/s | 30 | High damage |

- **Recruitment:** Click a Lair → opens recruit menu → select monster → deduct gold → spawn at Lair tile
- **AI:** Monsters have an aggro radius of 3 tiles. If a hero enters radius, monster moves to attack. Otherwise, idle.

### 3.6 Heroes

- **Goal:** Pathfind to Dungeon Heart and destroy it.
- **Spawning:** Enter from map edges (random valid edge tile).
- **Stats (per wave):**

| Wave | Hero Type | Count | HP | Damage | Move Speed |
|------|-----------|-------|----|--------|------------|
| 1 | Adventurer | 3 | 40 | 5 | 1.5 tiles/s |
| 2 | Adventurer | 4 | 40 | 5 | 1.5 tiles/s |
| 2 | Knight | 2 | 80 | 8 | 1.2 tiles/s |
| 3 | Adventurer | 5 | 40 | 5 | 1.5 tiles/s |
| 3 | Knight | 3 | 80 | 8 | 1.2 tiles/s |
| 3 | Paladin | 1 | 150 | 12 | 1.0 tiles/s |

- **Pathfinding:** A* to Dungeon Heart tile. Recalculate every 0.5s or when path is blocked.
- **Combat:** Heroes attack the nearest monster or room blocking their path. If nothing blocks, attack Dungeon Heart.

### 3.7 Trap Room

- **Effect:** Any hero on a directly adjacent floor tile takes 5 damage per second.
- **Visual:** Spikes or flame animation on adjacent tiles.
- **Stacking:** Multiple Trap Rooms can affect the same hero (damage stacks).

### 3.8 Pause System

- **Toggle:** Spacebar or UI button
- **Paused State:**
  - All entities freeze (no movement, no combat ticks)
  - Player CAN build rooms
  - Player CAN recruit monsters
  - Player CANNOT place traps during pause (optional balance rule)
- **Visual:** Slight dark overlay + "PAUSED" text

## 4. Combat System

### 4.1 Attack Resolution
```
if distance(attacker, target) <= attacker.range and attacker.cooldown <= 0:
    target.hp -= attacker.damage
    attacker.cooldown = 1.0 / attacker.attack_speed
    if target.hp <= 0:
        target.die()
        if target is Hero:
            gold += 10
```

### 4.2 Death
- Entity removed from active list
- Death animation (flash white → fade out, 0.3s)
- If Dungeon Heart dies → trigger Loss
- If all waves cleared and no heroes remain → trigger Win

## 5. Input Mapping

| Input | Action |
|-------|--------|
| Left Click (grid) | Select tile / build room (if build mode active) |
| Left Click (UI) | Press buttons, recruit monsters |
| Spacebar | Toggle pause |
| ESC | Deselect current tool / cancel build |

## 6. UI Specification

### 6.1 Sidebar Layout (256x384, right side)

```
+------------------+
|  GOLD: 150       |  <- Top, large text
+------------------+
| [LAIR] [TRAP]    |  <- Build buttons, 2 per row
| [TREASURY] [?]   |
+------------------+
| Wave: 1 / 3      |  <- Wave counter
| Heroes: 3 alive  |  <- Live enemy count
+------------------+
| [PAUSE]          |  <- Pause button
+------------------+
| Selected: None   |  <- Context info
+------------------+
| (Empty space     |
|  for future UI)  |
+------------------+
```

### 6.2 Button States
- **Default:** Dark stone background, light border
- **Hover:** Brighter border
- **Active/Pressed:** Inset shadow, darker background
- **Disabled:** Grayed out, cannot click (insufficient gold)

## 7. Art Specification (Designer Deliverables)

### 7.1 Color Palette (Dark Fantasy)

| Name | Hex | Usage |
|------|-----|-------|
| Void Black | `#0d0d0d` | Background, UI backing |
| Stone Gray | `#4a4a4a` | Floor tiles |
| Wall Gray | `#2b2b2b` | Wall tiles |
| Moss Green | `#3d5c3a` | Accent on stone |
| Slime Green | `#6bbf47` | Slime units |
| Goblin Skin | `#5c8a45` | Goblin units |
| Bone White | `#d4d4d4` | Skeleton units |
| Hero Red | `#c94c4c` | Hero cloaks |
| Knight Steel | `#8a9bb8` | Knight armor |
| Paladin Gold | `#d4af37` | Paladin trim |
| Heart Purple | `#8a2be2` | Dungeon Heart glow |
| Gold Yellow | `#ffd700` | UI gold icon, treasury |
| Trap Orange | `#cc5500` | Trap room, fire accents |
| Blood Red | `#8b0000` | Damage indicators |
| UI Border | `#7a7a7a` | Panel borders |

### 7.2 Asset List

#### Tiles (32x32)
- `tile_stone_floor.png`
- `tile_stone_wall.png`
- `tile_dungeon_heart.png` (animated: pulse glow, 2 frames)
- `tile_lair.png`
- `tile_trap_room.png`
- `tile_treasury.png`

#### Units (32x32)
- `unit_goblin_idle.png` (2-frame idle)
- `unit_slime_idle.png` (2-frame idle, squish)
- `unit_skeleton_idle.png` (2-frame idle)
- `unit_hero_adventurer.png` (2-frame walk)
- `unit_hero_knight.png` (2-frame walk)
- `unit_hero_paladin.png` (2-frame walk)

#### UI
- `ui_panel.png` (256x384 or 9-slice)
- `ui_button_default.png` (64x32)
- `ui_button_hover.png` (64x32)
- `ui_button_disabled.png` (64x32)
- `ui_gold_icon.png` (16x16)
- `ui_cursor_build.png` (16x16)
- `ui_cursor_select.png` (16x16)

#### Effects
- `effect_damage.png` (8x8, red flash)
- `effect_death.png` (16x16, fade particle)

## 8. File Structure

```
dungeon-keep/
├── SPEC.md                  # This document
├── README.md                # Setup and run instructions
├── requirements.txt         # Python dependencies (pygame, pygbag)
├── main.py                  # Entry point, game loop, state machine
├── constants.py             # Colors, dimensions, tile sizes, enums
├── assets.py                # Asset loading, sprite registry
├── grid.py                  # Tile map, pathfinding (A*)
├── entities.py              # Entity base, Monster, Hero, Room (as entity?)
├── combat.py                # Damage resolution, targeting, cooldowns
├── waves.py                 # Wave definitions, spawning logic
├── ui.py                    # Buttons, panels, sidebar, HUD
├── renderer.py              # All draw calls, camera, scaling
├── input_handler.py         # Mouse/keyboard event translation
├── game_state.py            # State machine (MENU, PLAYING, PAUSED, WIN, LOSS)
├── build_system.py          # Room placement validation, cost deduction
└── assets/
    ├── tiles/
    │   ├── tile_stone_floor.png
    │   ├── tile_stone_wall.png
    │   ├── tile_dungeon_heart.png
    │   ├── tile_lair.png
    │   ├── tile_trap_room.png
    │   └── tile_treasury.png
    ├── units/
    │   ├── unit_goblin_idle.png
    │   ├── unit_slime_idle.png
    │   ├── unit_skeleton_idle.png
    │   ├── unit_hero_adventurer.png
    │   ├── unit_hero_knight.png
    │   └── unit_hero_paladin.png
    ├── ui/
    │   ├── ui_panel.png
    │   ├── ui_button_default.png
    │   ├── ui_button_hover.png
    │   ├── ui_button_disabled.png
    │   ├── ui_gold_icon.png
    │   ├── ui_cursor_build.png
    │   └── ui_cursor_select.png
    └── effects/
        ├── effect_damage.png
        └── effect_death.png
```

## 9. Module API Contracts

### 9.1 `constants.py`
```python
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 384
GRID_WIDTH = 16
GRID_HEIGHT = 12
TILE_SIZE = 32
PLAY_AREA_WIDTH = 512  # 16 * 32
SIDEBAR_WIDTH = 256
SCALE_FACTOR = 2
FPS = 60

class TileType(Enum):
    STONE_WALL = auto()
    STONE_FLOOR = auto()
    DUNGEON_HEART = auto()
    LAIR = auto()
    TRAP_ROOM = auto()
    TREASURY = auto()

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    WIN = auto()
    LOSS = auto()
```

### 9.2 `grid.py`
```python
class Grid:
    def __init__(self, width: int, height: int) -> None: ...
    def in_bounds(self, x: int, y: int) -> bool: ...
    def is_walkable(self, x: int, y: int) -> bool: ...
    def is_buildable(self, x: int, y: int) -> bool: ...
    def get_tile(self, x: int, y: int) -> TileType: ...
    def set_tile(self, x: int, y: int, tile_type: TileType) -> None: ...
    def get_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]: ...
    def find_dungeon_heart(self) -> Tuple[int, int]: ...
```

### 9.3 `entities.py`
```python
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class CombatStats:
    hp: int
    max_hp: int
    damage: int
    attack_speed: float  # attacks per second
    attack_range: float  # in tiles
    attack_cooldown: float = 0.0

class Entity:
    def __init__(self, grid_x: int, grid_y: int, stats: CombatStats) -> None: ...
    @property
    def position(self) -> Tuple[float, float]: ...  # pixel coordinates, float for smooth movement
    def update(self, dt: float, grid: Grid, all_entities: List['Entity']) -> None: ...
    def take_damage(self, amount: int) -> None: ...
    @property
    def is_alive(self) -> bool: ...
    def die(self) -> None: ...

class Monster(Entity):
    def __init__(self, grid_x: int, grid_y: int, monster_type: str) -> None: ...
    def find_target(self, heroes: List['Hero']) -> Optional['Hero']: ...

class Hero(Entity):
    def __init__(self, grid_x: int, grid_y: int, hero_type: str) -> None: ...
    def set_path(self, path: List[Tuple[int, int]]) -> None: ...
    def update_pathfinding(self, grid: Grid) -> None: ...
```

### 9.4 `combat.py`
```python
def resolve_combat(attacker: Entity, target: Entity, dt: float) -> bool:
    """Process one combat tick. Returns True if target died."""
    ...

def find_nearest_enemy(entity: Entity, enemies: List[Entity], max_range: float) -> Optional[Entity]:
    ...

def apply_trap_damage(heroes: List[Hero], grid: Grid, dt: float) -> None:
    """Apply damage to heroes adjacent to trap rooms."""
    ...
```

### 9.5 `waves.py`
```python
@dataclass
class Wave:
    wave_number: int
    spawns: List[Tuple[str, int]]  # (hero_type, count)
    spawn_interval: float  # seconds between spawns

WAVES: List[Wave] = [...]

class WaveManager:
    def __init__(self, waves: List[Wave]) -> None: ...
    def start_wave(self, wave_index: int) -> None: ...
    def update(self, dt: float, grid: Grid) -> List[Hero]: ...  # returns newly spawned heroes
    @property
    def all_waves_complete(self) -> bool: ...
    @property
    def current_wave(self) -> int: ...
```

### 9.6 `build_system.py`
```python
class BuildSystem:
    def __init__(self, grid: Grid, starting_gold: int = 150) -> None: ...
    @property
    def gold(self) -> int: ...
    def can_build(self, x: int, y: int, room_type: TileType) -> bool: ...
    def build(self, x: int, y: int, room_type: TileType) -> bool: ...
    def can_recruit(self, lair_x: int, lair_y: int, monster_type: str) -> bool: ...
    def recruit(self, lair_x: int, lair_y: int, monster_type: str) -> Optional[Monster]: ...
    def add_gold(self, amount: int) -> None: ...
```

### 9.7 `ui.py`
```python
class UI:
    def __init__(self, build_system: BuildSystem, wave_manager: WaveManager) -> None: ...
    def handle_event(self, event: pygame.event.Event) -> Optional[UIAction]: ...
    def draw(self, surface: pygame.Surface) -> None: ...
    def update(self, dt: float) -> None: ...

@dataclass
class UIAction:
    action_type: str  # 'build', 'recruit', 'pause', 'restart'
    payload: dict
```

### 9.8 `renderer.py`
```python
class Renderer:
    def __init__(self, screen: pygame.Surface, scale: int = 2) -> None: ...
    def clear(self) -> None: ...
    def draw_grid(self, grid: Grid, assets: AssetRegistry) -> None: ...
    def draw_entity(self, entity: Entity, assets: AssetRegistry) -> None: ...
    def draw_ui(self, ui: UI) -> None: ...
    def present(self) -> None: ...  # blit to screen
```

## 10. Milestones & Acceptance Criteria

### Milestone 1: Skeleton (Architecture & Rendering)
**Goal:** A running window with a grid, clickable tiles, and placeholder colored rectangles.

**AC:**
- [ ] Window opens at 768x384 (scaled to 1536x768)
- [ ] 16x12 grid renders with distinct colors for floor and wall
- [ ] Dungeon Heart placed at center
- [ ] Left-clicking a tile logs its coordinates
- [ ] Game loop runs at stable 60 FPS
- [ ] Title screen → Game screen transition works
- [ ] `assets/` directory exists with placeholder PNGs (colored squares)

**Est. Effort:** Senior Dev — 1 session

---

### Milestone 2: Build & Economy
**Goal:** Player can build rooms and gold is tracked.

**AC:**
- [ ] Sidebar UI renders with build buttons
- [ ] Clicking a build button enters "build mode"
- [ ] Clicking a valid floor tile places the room and deducts gold
- [ ] Invalid tiles (walls, occupied, insufficient gold) reject with visual feedback
- [ ] Treasury passively generates gold
- [ ] Gold counter updates in real-time
- [ ] Trap room shows visual indicator on adjacent tiles

**Est. Effort:** Senior Dev — 1 session

---

### Milestone 3: Units & Combat
**Goal:** Monsters and heroes exist, fight, and die.

**AC:**
- [ ] Clicking a Lair opens recruit menu
- [ ] Recruiting spawns monster at Lair location
- [ ] Heroes spawn at map edge and move toward Dungeon Heart
- [ ] Heroes path around walls and rooms
- [ ] Monsters aggro heroes within 3 tiles
- [ ] Combat deals damage based on stats
- [ ] Death removes entity and awards gold (heroes only)
- [ ] All stats use `dt` for frame-rate independence

**Est. Effort:** Senior Dev — 1–2 sessions | Designer — deliver unit sprites

---

### Milestone 4: Waves & Polish
**Goal:** Complete game loop with win/lose conditions and final art.

**AC:**
- [ ] 3 waves spawn according to spec
- [ ] Spacebar toggles pause; build/recruit allowed while paused
- [ ] Dungeon Heart destruction triggers Loss screen
- [ ] Surviving all waves with no heroes remaining triggers Win screen
- [ ] All placeholder art replaced with final pixel art
- [ ] Death flash animation plays
- [ ] Restart button returns to fresh game state
- [ ] `pygbag` builds successfully and runs in browser

**Est. Effort:** Senior Dev — 1 session | Designer — final asset pass

## 11. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| A* pathfinding too slow on grid | Low | Medium | Grid is only 16x12; precalculate if needed |
| Pygbag WASM build fails | Medium | High | Test build at M1; keep dependencies minimal |
| Art delivery delayed | Medium | Medium | Use colored rectangles as drop-in replacements |
| Scope creep (multi-tile rooms, tech tree) | High | High | PM gate; update SPEC.md via PR only |
| Frame drops with many entities | Low | Medium | Cap max monsters/heroes; pool entities |

## 12. Session Continuity & Development Workflow

### 12.1 Ticket-First Development
- **Before implementing any feature, fix, or refactor:** create a ticket/issue entry in `state.md` describing what will be done.
- The ticket must include: title, description, affected files, and expected outcome.
- No code changes should begin until the ticket is recorded in `state.md`.

### 12.2 State Persistence (`state.md`)
- At the end of every session (or when the user says "save state"), update `state.md` with:
  - Current milestone progress
  - Open tickets/issues
  - Recently completed work
  - Blockers or decisions pending
  - Next steps / todo list
- `state.md` is the handoff document for continuing work in a new session.
- Keep it concise but complete enough that a fresh session can pick up without context loss.

### 12.3 Commit and Push
- **After every meaningful change** (feature completion, bug fix, milestone boundary, or session end): commit with a descriptive message.
- **After every commit:** push to the remote repository (`git push origin main`).
- **Never leave unpushed commits** at the end of a session.

## 13. Changelog

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-09-24 | 0.1.0 | PM + Senior Dev | Initial spec |

---
*This SPEC is the source of truth. Any deviation requires a PR with PM approval.*
