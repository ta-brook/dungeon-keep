# Dungeon Keep — Color Palette Reference

## Design Principles
- **Restricted palette:** 15 colors total for consistency and retro feel
- **Dark fantasy:** Muted tones with selective accent colors for readability
- **Functional color coding:** Unit types and UI elements have distinct colors for instant recognition

## Base Colors

| ID | Name | Hex | RGB | Usage |
|----|------|-----|-----|-------|
| C01 | Void Black | `#0d0d0d` | 13, 13, 13 | Background, UI backing, shadows |
| C02 | Stone Gray | `#4a4a4a` | 74, 74, 74 | Floor tiles, inactive UI |
| C03 | Wall Gray | `#2b2b2b` | 43, 43, 43 | Wall tiles, stone borders |
| C04 | Moss Green | `#3d5c3a` | 61, 92, 58 | Floor accent, organic stone |
| C05 | UI Border | `#7a7a7a` | 122, 122, 122 | Panel borders, dividers |

## Unit Colors

| ID | Name | Hex | RGB | Usage |
|----|------|-----|-----|-------|
| C06 | Slime Green | `#6bbf47` | 107, 191, 71 | Slime units, poison effects |
| C07 | Goblin Skin | `#5c8a45` | 92, 138, 69 | Goblin units, orc-ish tones |
| C08 | Bone White | `#d4d4d4` | 212, 212, 212 | Skeleton units, bone details |
| C09 | Hero Red | `#c94c4c` | 201, 76, 76 | Adventurer cloaks, danger indicators |
| C10 | Knight Steel | `#8a9bb8` | 138, 155, 184 | Knight armor, metallic UI accents |
| C11 | Paladin Gold | `#d4af37` | 212, 175, 55 | Paladin trim, treasure highlights |

## Effect & Accent Colors

| ID | Name | Hex | RGB | Usage |
|----|------|-----|-----|-------|
| C12 | Heart Purple | `#8a2be2` | 138, 43, 226 | Dungeon Heart glow, magic effects |
| C13 | Gold Yellow | `#ffd700` | 255, 215, 0 | Gold UI icon, treasury sparkle |
| C14 | Trap Orange | `#cc5500` | 204, 85, 0 | Trap rooms, fire, warning indicators |
| C15 | Blood Red | `#8b0000` | 139, 0, 0 | Damage numbers, death particles |

## Color Pairing Rules

### Contrast Requirements
- **Text on dark background:** Use C13 (Gold), C12 (Purple), or C15 (Blood) for emphasis
- **Text on light background:** Use C01 (Void Black) or C03 (Wall Gray)
- **UI buttons:** Border C05, background C03, text C13
- **Disabled buttons:** All C02 with 50% opacity

### Monster Team Identity
- Monsters use greens (C06, C07) + bone (C08) to signal "dungeon/native"
- Heroes use warm colors (C09, C11) + steel (C10) to signal "invader/armored"

### Health Bars
- Background: C03 (Wall Gray)
- Fill (healthy): C06 (Slime Green)
- Fill (damaged): C14 (Trap Orange)
- Fill (critical): C15 (Blood Red)

## Shading Convention
- **Light source:** Top-left
- **Highlight:** Add 20% brightness to base color
- **Shadow:** Subtract 20% brightness, shift toward C01
- **Outline:** 1px C01 (Void Black) on all sprites for readability

## Export Notes
- All sprites use indexed color mode with this exact palette
- No anti-aliasing; hard pixel edges only
- Transparency: Full alpha for empty pixels, no semi-transparent edges
