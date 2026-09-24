# Dungeon Keep — Asset Manifest

## Naming Convention
```
{category}_{name}_{variant}.{ext}
```
- **category:** `tile`, `unit`, `ui`, `effect`
- **name:** descriptive slug (e.g., `stone_floor`, `goblin`)
- **variant:** `idle`, `walk`, `attack`, `default`, `hover`, etc.
- **ext:** always `.png`

## Tiles (assets/tiles/)

### Static Tiles (1 frame)

| Filename | Size | Frames | Pivot | Palette IDs | Notes |
|----------|------|--------|-------|-------------|-------|
| `tile_stone_floor.png` | 32×32 | 1 | center | C02, C04 | Subtle moss variation |
| `tile_stone_wall.png` | 32×32 | 1 | center | C03, C05 | Cracked stone texture |
| `tile_lair.png` | 32×32 | 1 | center | C03, C06, C12 | Organic/nest-like structure |
| `tile_trap_room.png` | 32×32 | 1 | center | C03, C14 | Mechanical base with spikes |
| `tile_treasury.png` | 32×32 | 1 | center | C03, C13 | Gold pile icon embedded |

### Animated Tiles (2 frames)

| Filename | Size | Frames | FPS | Pivot | Palette IDs | Notes |
|----------|------|--------|-----|-------|-------------|-------|
| `tile_dungeon_heart.png` | 32×32 | 2 | 2 | center | C12, C01 | Pulse: full glow → dim glow |

## Units (assets/units/)

### Monster Sprites (2-frame idle)

| Filename | Size | Frames | FPS | Pivot | Palette IDs | Notes |
|----------|------|--------|-----|-------|-------------|-------|
| `unit_goblin_idle.png` | 32×32 | 2 | 3 | bottom-center | C07, C01 | Bounce: standing → crouch |
| `unit_slime_idle.png` | 32×32 | 2 | 2 | bottom-center | C06, C01 | Squish: tall → flat |
| `unit_skeleton_idle.png` | 32×32 | 2 | 2 | bottom-center | C08, C01 | Rattle: still → slight shake |

### Hero Sprites (2-frame walk)

| Filename | Size | Frames | FPS | Pivot | Palette IDs | Notes |
|----------|------|--------|-----|-------|-------------|-------|
| `unit_hero_adventurer.png` | 32×32 | 2 | 4 | bottom-center | C09, C01 | Walk cycle: left foot → right foot |
| `unit_hero_knight.png` | 32×32 | 2 | 3 | bottom-center | C10, C01 | Heavy walk: slower, armor bob |
| `unit_hero_paladin.png` | 32×32 | 2 | 3 | bottom-center | C11, C10, C01 | Slow march, cape sway |

## UI (assets/ui/)

### Panel & Background

| Filename | Size | Frames | Pivot | Palette IDs | Notes |
|----------|------|--------|-------|-------------|-------|
| `ui_panel.png` | 256×384 | 1 | top-left | C03, C05 | Sidebar panel background |
| `ui_button_default.png` | 64×32 | 1 | center | C03, C05 | Standard button state |
| `ui_button_hover.png` | 64×32 | 1 | center | C03, C13 | Brighter border highlight |
| `ui_button_disabled.png` | 64×32 | 1 | center | C02, C05 | Grayed out, 50% opacity |
| `ui_button_pressed.png` | 64×32 | 1 | center | C01, C05 | Dark inset, active state |

### Icons

| Filename | Size | Frames | Pivot | Palette IDs | Notes |
|----------|------|--------|-------|-------------|-------|
| `ui_gold_icon.png` | 16×16 | 1 | center | C13 | Coin icon for HUD |
| `ui_heart_icon.png` | 16×16 | 1 | center | C12 | Dungeon Heart health icon |
| `ui_wave_icon.png` | 16×16 | 1 | center | C15 | Skull/sword wave indicator |

### Cursors

| Filename | Size | Frames | Pivot | Palette IDs | Notes |
|----------|------|--------|-------|-------------|-------|
| `ui_cursor_select.png` | 16×16 | 1 | top-left | C13 | Default pointer |
| `ui_cursor_build.png` | 16×16 | 1 | top-left | C14 | Hammer icon, build mode |
| `ui_cursor_recruit.png` | 16×16 | 1 | top-left | C12 | Summon/magic icon |

## Effects (assets/effects/)

| Filename | Size | Frames | FPS | Pivot | Palette IDs | Notes |
|----------|------|--------|-----|-------|-------------|-------|
| `effect_damage.png` | 8×8 | 1 | center | C15 | Red flash overlay on hit |
| `effect_death.png` | 16×16 | 4 | 8 | center | C15, C01 | Cross dissolve fade out |
| `effect_build.png` | 32×32 | 4 | 10 | center | C13 | Sparkle on room placement |
| `effect_trap_spike.png` | 32×32 | 2 | 4 | center | C14 | Spike popup on trap trigger |

## Placeholder Generation

Until final art is ready, Senior Dev should generate these as colored rectangles:

```python
# Placeholder colors (RGB tuples)
PLACEHOLDERS = {
    "tile_stone_floor": (74, 74, 74),
    "tile_stone_wall": (43, 43, 43),
    "tile_dungeon_heart": (138, 43, 226),
    "tile_lair": (61, 92, 58),
    "tile_trap_room": (204, 85, 0),
    "tile_treasury": (255, 215, 0),
    "unit_goblin": (92, 138, 69),
    "unit_slime": (107, 191, 71),
    "unit_skeleton": (212, 212, 212),
    "unit_hero_adventurer": (201, 76, 76),
    "unit_hero_knight": (138, 155, 184),
    "unit_hero_paladin": (212, 175, 55),
}
```

## Delivery Order (Priority)

1. **M1 placeholders** — All tiles + basic unit rectangles
2. **M2 additions** — UI panel, buttons, icons, build cursor
3. **M3 additions** — Final unit sprites (monsters + heroes), damage effect
4. **M4 additions** — Death animation, build sparkle, trap spike, button hover/pressed states
