# Dungeon Keep — Sprite Sheet Layouts

## Format Specification

- **Orientation:** Horizontal sprite sheets (frames left-to-right)
- **Frame size:** 32×32 for units/tiles, variable for UI
- **Spacing:** 0px between frames (tight packing)
- **Total sheet size:** `(frame_width * frame_count) × frame_height`
- **Metadata:** Frame count implied by filename or stored in `assets/manifest.json`

## Unit Sprite Sheets

### Idle Animations (Monsters)

#### unit_goblin_idle.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Stand  │ Crouch │
│ [██    │  [██   │
│  ██    │   ██   │
│ ▓▓▓   │  ▓▓▓  │
└────────┴────────┘
```
- **Frame 0:** Standing upright, arms at sides
- **Frame 1:** Slight crouch, arms forward (anticipation)
- **Timing:** 333ms per frame (3 FPS)
- **Loop:** Ping-pong (0→1→0)

#### unit_slime_idle.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Tall   │ Flat   │
│  ┌┐    │        │
│ /██\   │  ████  │
│ \██/   │  ████  │
└────────┴────────┘
```
- **Frame 0:** Tall, rounded shape
- **Frame 1:** Squished flat, wider
- **Timing:** 500ms per frame (2 FPS)
- **Loop:** Ping-pong

#### unit_skeleton_idle.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Still  │ Rattle │
│  ○     │  ○     │
│ /█\    │  █     │
│ / \   │ / \   │
└────────┴────────┘
```
- **Frame 0:** Static pose
- **Frame 1:** Slight offset/shake (1px right, subtle)
- **Timing:** 500ms per frame (2 FPS)
- **Loop:** Ping-pong

### Walk Animations (Heroes)

#### unit_hero_adventurer.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Left   │ Right  │
│  /○    │  ○\   │
│ /██    │   ██\  │
│  / \   │  / \   │
└────────┴────────┘
```
- **Frame 0:** Left foot forward, slight lean
- **Frame 1:** Right foot forward, slight lean
- **Timing:** 250ms per frame (4 FPS)
- **Loop:** Cycle forward

#### unit_hero_knight.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Step   │ Step   │
│  [○]   │  [○]   │
│  [██]  │  [██]  │
│  /▓\   │  \▓/   │
└────────┴────────┘
```
- **Frame 0:** Heavy step left, armor bob down
- **Frame 1:** Heavy step right, armor bob up
- **Timing:** 333ms per frame (3 FPS)
- **Loop:** Cycle forward

#### unit_hero_paladin.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ March  │ March  │
│  +○+   │  +○+   │
│  ███   │  ███   │
│  / \   │  | |   │
└────────┴────────┘
```
- **Frame 0:** Left foot forward, cape sway left
- **Frame 1:** Right foot forward, cape sway right
- **Timing:** 333ms per frame (3 FPS)
- **Loop:** Cycle forward

## Tile Sprite Sheets

### tile_dungeon_heart.png
```
Sheet size: 64×32
┌────────┬────────┐
│ Frame 0│ Frame 1│
│ Bright │ Dim    │
│  💜    │  💜    │
│ (glow) │ (faint)│
└────────┴────────┘
```
- **Frame 0:** Full purple glow, bright center
- **Frame 1:** Dimmed, 60% brightness
- **Timing:** 500ms per frame (2 FPS)
- **Loop:** Ping-pong

## Effect Sprite Sheets

### effect_death.png
```
Sheet size: 64×16
┌────────┬────────┬────────┬────────┐
│Frame 0 │Frame 1 │Frame 2 │Frame 3 │
│ Solid  │ Fade   │ Fade   │ Gone   │
│  ████  │  ▓▓▓▓  │  ░░░░  │  ····  │
└────────┴────────┴────────┴────────┘
```
- **Frame 0:** Full opacity red/blood
- **Frame 1:** 66% opacity
- **Frame 2:** 33% opacity
- **Frame 3:** 0% opacity (remove entity)
- **Timing:** 125ms per frame (8 FPS)
- **Loop:** Play once, then destroy

### effect_build.png
```
Sheet size: 128×32
┌────────┬────────┬────────┬────────┐
│Frame 0 │Frame 1 │Frame 2 │Frame 3 │
│ Spark  │ Spark  │ Spark  │ Fade   │
│   ✦    │  ✦✦✦   │   ✦    │  ···   │
└────────┴────────┴────────┴────────┘
```
- **Frames 0-2:** Gold sparkles expanding outward
- **Frame 3:** Fade to nothing
- **Timing:** 100ms per frame (10 FPS)
- **Loop:** Play once

### effect_trap_spike.png
```
Sheet size: 64×32
┌────────┬────────┐
│Frame 0 │Frame 1 │
│ Down   │ Up     │
│  ───   │  ▲▲▲   │
└────────┴────────┘
```
- **Frame 0:** Spikes retracted (floor level)
- **Frame 1:** Spikes extended (damage active)
- **Timing:** 250ms per frame (4 FPS)
- **Loop:** Ping-pong when hero is on tile

## Rendering Notes for Senior Dev

```python
# Sprite sheet rendering helper
def draw_sprite_sheet(
    surface: pygame.Surface,
    sheet: pygame.Surface,
    frame_index: int,
    frame_width: int,
    frame_height: int,
    x: int,
    y: int
) -> None:
    """Draw a single frame from a horizontal sprite sheet."""
    rect = pygame.Rect(
        frame_index * frame_width,
        0,
        frame_width,
        frame_height
    )
    surface.blit(sheet, (x, y), rect)

# Animation timing
def get_current_frame(
    frame_count: int,
    fps: float,
    elapsed_time: float,
    loop: bool = True
) -> int:
    """Calculate current frame index based on elapsed time."""
    frame_duration = 1.0 / fps
    total_duration = frame_count * frame_duration
    
    if loop:
        t = elapsed_time % total_duration
    else:
        t = min(elapsed_time, total_duration - frame_duration)
    
    return int(t / frame_duration) % frame_count
```

## Asset Loading Strategy

1. **Preload at startup:** Load all `.png` files into `AssetRegistry`
2. **Sheet splitting:** Store full sheet; extract frames on demand
3. **Animation state:** Each entity tracks its own `animation_timer`
4. **Memory:** Total asset memory ~100KB (very small, no streaming needed)
