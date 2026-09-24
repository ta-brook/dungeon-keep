# Dungeon Keep — UI Mockup Specification

## Screen Layout

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  PLAY AREA (512×384)         │  SIDEBAR (256×384)          │
│                              │                              │
│  ┌────────────────────────┐  │  ┌────────────────────────┐  │
│  │                        │  │  │  GOLD: 150             │  │
│  │    16×12 GRID          │  │  │  [coin icon]           │  │
│  │                        │  │  ├────────────────────────┤  │
│  │  Each tile: 32×32 px   │  │  │                        │  │
│  │                        │  │  │  BUILD                 │  │
│  │  [Dungeon Heart at     │  │  │  ┌────┐ ┌────┐        │  │
│  │   center ~ (8,6)]      │  │  │  │LAIR│ │TRAP│        │  │
│  │                        │  │  │  └────┘ └────┘        │  │
│  │                        │  │  │  ┌────┐ ┌────┐        │  │
│  │                        │  │  │  │TRES│ │ -- │        │  │
│  │                        │  │  │  └────┘ └────┘        │  │
│  │                        │  │  ├────────────────────────┤  │
│  │                        │  │  │                        │  │
│  │                        │  │  │  WAVE INFO             │  │
│  │                        │  │  │  Wave: 1 / 3           │  │
│  │                        │  │  │  Heroes: 3 alive       │  │
│  │                        │  │  │  [skull icon]          │  │
│  │                        │  │  ├────────────────────────┤  │
│  │                        │  │  │                        │  │
│  │                        │  │  │  [  PAUSE  ]           │  │
│  │                        │  │  │                        │  │
│  │                        │  │  ├────────────────────────┤  │
│  │                        │  │  │  Selected: None        │  │
│  │                        │  │  │  (context info here)   │  │
│  │                        │  │  └────────────────────────┘  │
│  └────────────────────────┘  └─────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
           TOTAL: 768×384 logical (1536×768 rendered)
```

## Sidebar Detailed Layout

```
SIDEBAR PANEL (256×384)
┌────────────────────────┐  ← y=0
│  HEADER: GOLD          │
│  ┌──┐  GOLD: 150       │
│  │🪙│  +1/sec          │  ← y=40
│  └──┘                  │
├────────────────────────┤  ← y=64
│  BUILD SECTION         │
│  Label: "BUILD"        │
│                        │
│  ┌────┐  ┌────┐        │
│  │LAIR│  │TRAP│        │  ← y=96, 96+72
│  │ 50 │  │ 40 │        │
│  └────┘  └────┘        │
│                        │
│  ┌────┐  ┌────┐        │
│  │TRES│  │    │        │  ← y=96+40, 96+72+40
│  │ 60 │  │    │        │
│  └────┘  └────┘        │
├────────────────────────┤  ← y=192
│  WAVE INFO SECTION     │
│  Label: "WAVE"         │
│                        │
│  Wave: 1 / 3           │
│  Heroes: 3 alive       │
│  [vvvvvvvvvvvv]        │  ← progress bar
├────────────────────────┤  ← y=288
│  CONTROLS              │
│                        │
│  ┌──────────────┐      │
│  │   [PAUSE]    │      │  ← y=304, centered
│  └──────────────┘      │
├────────────────────────┤  ← y=340
│  CONTEXT INFO          │
│  Selected: None        │
│  (tile coords,         │
│   room info, etc.)     │
└────────────────────────┘  ← y=384
```

## Button Specifications

### Build Button (64×32)
```
┌────────────────────────┐
│  [Icon]  ROOM_NAME     │  ← 16×16 icon left, text right
│          50g           │  ← cost below name
└────────────────────────┘
```

**States:**
- **Default:** Background C03, border C05, text C13
- **Hover:** Border brightens to C13, subtle glow
- **Pressed:** Background darkens to C01, inset border
- **Disabled:** Background C02, text C05, 50% opacity, "LOCKED" text

### Pause Button (128×32)
- Centered in controls section
- Large text: "PAUSE" / "RESUME"
- Background C03, text C13
- Pressed: Background C01, text C14

## Typography

- **Font:** System monospace or pixel font (Press Start 2P style)
- **Sizes:**
  - Title: 24px
  - Section headers: 16px
  - Body text: 12px
  - Button labels: 10px
- **Colors:**
  - Headers: C13 (Gold)
  - Body: C05 (UI Border)
  - Emphasis: C12 (Purple) or C15 (Blood)

## Interactions

### Hover States
- Tile hover: 32×32 highlight rectangle, C13 at 30% opacity
- Button hover: Bright border, cursor change
- Unit hover: Show HP bar and name tooltip

### Selection Feedback
- Selected tile: Animated dashed border, C13
- Build mode active: Cursor changes to `ui_cursor_build.png`
- Recruit mode active: Cursor changes to `ui_cursor_recruit.png`

## Responsive Notes
- Sidebar width fixed at 256px
- Play area fills remaining width
- On window resize: maintain aspect ratio, letterbox if needed
