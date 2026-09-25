# Dungeon Keep Prototype — Specification

## 1. Game Concept

**Dungeon Keep** is a real-time-with-pause dungeon management and guild simulation game. The player builds rooms, recruits monsters, defends their Dungeon Heart against waves of invading heroes, and — inspired by the guild management genre — recruits guild members, assigns professions, crafts items, raids dungeons, and trades at an auction house.

- **Perspective:** Top-down 2D grid (expandable with camera scrolling from M5)
- **Theme:** Dark fantasy dungeon / guild management
- **Core Loop (M1–M4):** Build → Recruit → Defend → Earn Gold → Expand
- **Core Loop (M5–M8):** Build → Recruit NPCs → Craft → Raid → Trade → Expand → Defend → Chronicle

## 2. Screen Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Title Screen│────▶│ Game Screen │────▶│ Win / Loss  │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
                           │                    │
              ┌────────────┼────────────┐       │
              ▼            ▼            ▼       │
        ┌──────────┐ ┌──────────┐ ┌────────┐   │
        │  Guild   │ │ Crafting │ │  Raid  │   │
        │  Panel   │ │  Panel   │ │  Panel │   │
        └──────────┘ └──────────┘ └────────┘   │
              │            │            │       │
              └────────────┼────────────┘       │
                           ▼                    │
                    ┌─────────────┐             │
                    │  Chronicle  │◀────────────┘
                    │  Summary    │
                    └─────────────┘
```

### 2.1 Title Screen
- Dark stone background
- Game title centered
- "Start Game" button
- Brief instruction text

### 2.2 Game Screen
- **M1–M4:** Main play area: 512x384 (left/top), UI sidebar: 256x384 (right)
- **M5+:** Main play area: 768x384 (expandable with camera), UI sidebar: 256x384 (right)
- Total logical resolution: **768x384** (M1–M4) → **1024x384** (M5+, scaled 2x to 2048x768)
- Sidebar contains tabbed panels: Build, Guild, Crafting, Raid, Auction, Codex, Chronicle

### 2.3 Win / Loss Screen
- Overlay on game screen
- Win: "Dungeon Secured!" + chronicle summary (NPCs recruited, items crafted, gold earned, raids completed)
- Loss: "Dungeon Heart Destroyed!" + chronicle summary
- "Restart" button

### 2.4 Sub-Panels (M5+)
- **Guild Panel:** List of guild members, portraits, traits, morale, profession assignment
- **Crafting Panel:** Recipe list, resource inventory, crafting queue
- **Raid Panel:** Dungeon selection, party formation, raid progress, battle log
- **Auction Panel:** Item listing, market demand, visitor log, bargain alerts
- **Codex Panel:** Category tabs, completion bars, milestone rewards
- **Chronicle Panel:** Scrollable event log with timestamps

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

### 3.9 NPC / Guild Member System

- **Guild Members** are unique NPCs with personalities, professions, and stats.
- **Recruitment:** Heroes defeated in combat have a chance to join the guild instead of dying. Special "wandering" NPCs also appear between waves.
- **Capacity:** Max 12 guild members at once (expandable via guild hall upgrades).
- **Personality Traits:** Each NPC has 2 traits from a pool of 20 (e.g., Brave, Lazy, Greedy, Cheerful, Grumpy, Loyal, Reckless, Cautious, Social, Loner).
- **Morale:** 0–100 scale. Affected by: combat wins (+), defeats (−), gold income (+), overcrowding (−), matching profession to personality (+).
- **Permadeath (Soft):** NPCs that fail a raid have a chance to "quit the guild" (leave permanently). Higher morale = lower quit chance.

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Unique name from a pool of 120 |
| `portrait_id` | str | Sprite reference for portrait |
| `traits` | List[str] | 2 personality traits |
| `profession` | str | Assigned role (see §3.10) |
| `morale` | int | 0–100 |
| `level` | int | 1–20 |
| `stats` | NPCStats | HP, ATK, DEF, SPD, profession bonuses |
| `state` | str | `idle`, `working`, `raiding`, `resting` |

### 3.10 Profession System

- Each NPC is assigned one profession. They produce goods passively while idle in the village.
- **Professions:**

| Profession | Building Required | Output | Rate |
|------------|-------------------|--------|------|
| Farmer | Farm | Herbs, Wheat | 1 per 30s |
| Alchemist | Alchemy Lab | Potions (random) | 1 per 60s |
| Cook | Kitchen | Meals (morale boost) | 1 per 45s |
| Blacksmith | Forge | Weapons, Armor | 1 per 90s |
| Enchanter | Enchanting Table | Scroll, Gems | 1 per 120s |
| Miner | Mine | Ore, Stone | 1 per 30s |
| Fisher | Dock | Fish, Rare Catches | 1 per 45s |

- **Skill Levels:** Each profession has levels 1–10. Higher level = faster production + better quality items.
- **XP Gain:** NPCs gain profession XP from working and from raiding. Level up every 100 XP × current level.

### 3.11 Crafting System

- **Resources:** Herbs, Ore, Fish, Wheat, Wood, Stone, Gems (gathered by professions).
- **Recipes:** Defined in a recipe table. Each recipe requires specific resources + profession level.
- **Recipe Categories:**

| Category | Examples | Use |
|----------|----------|-----|
| Potions | Health Potion, Strength Potion, Speed Potion | Equip on raid party |
| Meals | Hearty Stew, Battle Feast | Morale boost before raid |
| Weapons | Iron Sword, Enchanted Staff | Equip on NPCs for raid stats |
| Armor | Leather Vest, Chain Mail | Equip on NPCs for raid defense |
| Scrolls | Fire Scroll, Shield Scroll | Consumable raid buffs |

- **Quality Tiers:** Common (white), Uncommon (green), Rare (blue), Epic (purple). Higher profession level = chance for higher quality.
- **Crafting Queue:** Player assigns NPCs to craft specific items. Items go to inventory.

### 3.12 Dungeon Raids (Offensive)

- **Concept:** Player forms a party of 1–4 guild members and sends them into a dungeon.
- **Dungeon List:** 3 dungeons available, each with increasing difficulty.

| Dungeon | Floors | Boss | Min Party Level | Rewards |
|---------|--------|------|-----------------|---------|
| Goblin Cave | 3 | Goblin King | 1 | Ore, Herbs, Gold |
| Sunken Temple | 5 | Sea Witch | 5 | Gems, Scrolls, Enchant Mats |
| Dragon's Lair | 7 | Ancient Dragon | 10 | Epic gear, Rare recipes, Gold |

- **Auto-Battle:** Raids are resolved automatically. The party fights through floors sequentially.
- **Battle Log:** After each raid, a log shows: damage dealt, items found, XP gained, casualties.
- **Raid Mechanics:**
  - Each floor has a monster encounter (auto-resolved using NPC stats + equipment).
  - Boss floor has a tougher encounter with guaranteed rare+ loot.
  - If party wipes, surviving NPCs may quit (morale check).
  - Raid duration: 30–120 seconds real-time (shown as a progress bar).
- **Cooldown:** NPCs that raid must rest for 60s before working or raiding again.

### 3.13 Trading / Auction House

- **Auction House:** A building where the player sells crafted items and resources for gold.
- **Mechanics:**
  - Player lists items with a price (or auto-price at market value).
  - "Visitors" (NPC buyers) appear periodically and purchase listed items.
  - **Market Demand:** Each item category has a demand level (Low / Normal / High) that fluctuates every 2 minutes.
  - High demand = items sell faster and at +20% price. Low demand = −20%.
  - **Bargain Events:** Occasionally, a visitor lists a rare item at a discount. Player can buy it.
- **Income:** Auction House is a major gold source alongside Treasury and hero kills.
- **Visitor Log:** Shows what sold, for how much, and what's in demand.

### 3.14 Village Expansion (Multi-Tile Buildings)

- **Transition from M2:** Rooms are 1-tile in M1–M4. Starting in M5, new buildings can be multi-tile.
- **Building Sizes:**

| Building | Size | Cost | Unlock |
|----------|------|------|--------|
| Farm | 2×2 | 80 gold | M5 |
| Alchemy Lab | 2×1 | 100 gold | M5 |
| Kitchen | 2×1 | 90 gold | M5 |
| Forge | 2×2 | 120 gold | M5 |
| Enchanting Table | 1×1 | 150 gold | M6 |
| Mine | 2×2 | 100 gold | M5 |
| Dock | 3×1 | 130 gold | M6 |
| Guild Hall | 3×3 | 200 gold | M5 |
| Auction House | 2×2 | 150 gold | M6 |

- **Grid Expansion:** Village area starts at 16×12. After M5, the grid expands to 24×18 (with camera scrolling) to accommodate buildings.
- **Placement Rules:** Buildings must be placed on `STONE_FLOOR`, cannot overlap other buildings, must have at least 1 tile of path access.
- **Decoration:** Optional cosmetic items (torches, banners, rugs) can be placed on floor tiles for morale bonus (+1 per decoration, max 10).

### 3.15 Codex / Progression System

- **Codex Categories:**

| Category | Tracks | Reward |
|----------|--------|--------|
| Alchemy | Potions crafted (unique) | Unlock higher-tier recipes |
| Cooking | Meals crafted (unique) | Morale bonus increase |
| Blacksmithing | Weapons/armor crafted | Unlock rare materials |
| Enchanting | Scrolls/gems crafted | Unlock epic tier |
| Farming | Crops harvested | Faster growth rate |
| Mining | Ore mined | Chance for rare ore |
| Fishing | Fish caught | Rare catch chance up |
| Raids | Dungeons cleared | Unlock harder dungeons |
| Collection | NPCs recruited | Unlock new NPC pool |

- **Completion %:** Each category shows X / Y discovered. Total completion shown on codex screen.
- **Milestones:** Hitting 25%, 50%, 75%, 100% in any category grants a permanent bonus (gold +5%, craft speed +10%, etc.).

### 3.16 Chronicle System

- **Event Log:** All significant events are recorded in a chronological "chronicle."
- **Events Tracked:**
  - NPC recruited (name, traits, profession)
  - NPC quit / died in raid
  - Building constructed
  - Rare item crafted
  - Dungeon boss defeated
  - Gold milestones (1000g, 5000g, 10000g)
  - Wave survived
  - NPC level up / profession level up
- **Display:** Scrollable text log in a dedicated UI panel. Each entry has a timestamp (wave number or game time).
- **Summary Screen:** On win/loss, the chronicle summary is shown (total events, NPCs recruited, items crafted, gold earned).

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
| Left Click (UI) | Press buttons, recruit monsters, interact with panels |
| Spacebar | Toggle pause |
| ESC | Deselect current tool / cancel build / close panel |
| Tab (M5+) | Cycle through sidebar panels (Build → Guild → Crafting → Raid → Auction → Codex → Chronicle) |
| Mouse Wheel (M5+) | Scroll chronicle log / recipe list |
| Right Click (M5+) | Camera drag (pan viewport) |

## 6. UI Specification

### 6.1 Sidebar Layout (256x384, right side)

**M1–M4 Layout:**
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

**M5+ Layout (Tabbed Panels):**
```
+------------------+
|  GOLD: 150       |  <- Top, large text (always visible)
+------------------+
| [Build][Guild]   |  <- Tab row (always visible)
| [Craft][Raid]    |
| [Auct][Codex]    |
| [Chron]          |
+------------------+
|                  |
|  Active Panel    |  <- Changes based on selected tab
|  Content         |
|                  |
+------------------+
| Wave: 1 / 3      |  <- Wave counter (always visible)
| Heroes: 3 alive  |  <- Live enemy count (always visible)
+------------------+
| [PAUSE]          |  <- Pause button (always visible)
+------------------+
```

### 6.2 Button States
- **Default:** Dark stone background, light border
- **Hover:** Brighter border
- **Active/Pressed:** Inset shadow, darker background
- **Disabled:** Grayed out, cannot click (insufficient gold)

### 6.3 Panel Specifications (M5+)

**Guild Panel:**
- List of guild members (portrait, name, traits, morale bar)
- Click member → detail view (stats, equipment, profession)
- "Assign Profession" dropdown (if building exists)
- Member count: X / 12

**Crafting Panel:**
- Resource inventory (icons + counts)
- Recipe list (filterable by category)
- Crafting queue (assigned NPC, progress bar)
- "Start Craft" button (disabled if insufficient resources)

**Raid Panel:**
- Dungeon list (name, floors, difficulty, rewards)
- Party formation (drag NPCs into 4 slots)
- "Start Raid" button (shows countdown)
- Battle log (scrollable, shows after raid)

**Auction Panel:**
- Item listing (inventory → list for sale)
- Market demand indicators (per category)
- Visitor log (who bought what)
- Bargain alerts (rare items at discount)

**Codex Panel:**
- Category tabs (Alchemy, Cooking, Blacksmithing, etc.)
- Completion bar (X / Y discovered)
- Milestone rewards (25%, 50%, 75%, 100%)
- Total completion percentage

**Chronicle Panel:**
- Scrollable event log
- Each entry: timestamp (wave #), icon, description
- Filter by event type (optional)
- "Highlights" toggle (major events only)

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
| Farm Green | `#4a7c3a` | Farm tiles, herbs |
| Alchemy Purple | `#6b3fa0` | Alchemy lab, potions |
| Forge Orange | `#b8560f` | Forge, weapons |
| Dock Blue | `#3a6b8a` | Dock, water |
| Guild Hall Brown | `#6b4a2a` | Guild hall, wood |
| Auction Teal | `#2a8a7a` | Auction house, market |
| Quality Common | `#d4d4d4` | Common item border |
| Quality Uncommon | `#4a7c3a` | Uncommon item border |
| Quality Rare | `#3a6b8a` | Rare item border |
| Quality Epic | `#6b3fa0` | Epic item border |
| Morale High | `#4a7c3a` | Morale bar (70-100) |
| Morale Mid | `#b8860b` | Morale bar (30-69) |
| Morale Low | `#8b0000` | Morale bar (0-29) |

### 7.2 Asset List

#### Tiles (32x32) — M1–M4
- `tile_stone_floor.png`
- `tile_stone_wall.png`
- `tile_dungeon_heart.png` (animated: pulse glow, 2 frames)
- `tile_lair.png`
- `tile_trap_room.png`
- `tile_treasury.png`

#### Tiles (32x32) — M5+ (Village Buildings)
- `tile_farm.png` (2x2 building)
- `tile_alchemy_lab.png` (2x1 building)
- `tile_kitchen.png` (2x1 building)
- `tile_forge.png` (2x2 building)
- `tile_enchanting_table.png` (1x1 building)
- `tile_mine.png` (2x2 building)
- `tile_dock.png` (3x1 building)
- `tile_guild_hall.png` (3x3 building)
- `tile_auction_house.png` (2x2 building)

#### Units (32x32) — M1–M4
- `unit_goblin_idle.png` (2-frame idle)
- `unit_slime_idle.png` (2-frame idle, squish)
- `unit_skeleton_idle.png` (2-frame idle)
- `unit_hero_adventurer.png` (2-frame walk)
- `unit_hero_knight.png` (2-frame walk)
- `unit_hero_paladin.png` (2-frame walk)

#### NPC Portraits (32x32) — M5+
- `npc_portrait_01.png` through `npc_portrait_30.png` (30 unique portraits)
- `npc_visitor_01.png` through `npc_visitor_10.png` (10 visitor/buyer portraits)

#### UI — M1–M4
- `ui_panel.png` (256x384 or 9-slice)
- `ui_button_default.png` (64x32)
- `ui_button_hover.png` (64x32)
- `ui_button_disabled.png` (64x32)
- `ui_gold_icon.png` (16x16)
- `ui_cursor_build.png` (16x16)
- `ui_cursor_select.png` (16x16)

#### UI — M5+ (Panels & Icons)
- `ui_guild_panel.png` (256x384 or 9-slice)
- `ui_crafting_panel.png` (256x384 or 9-slice)
- `ui_auction_panel.png` (256x384 or 9-slice)
- `ui_codex_panel.png` (256x384 or 9-slice)
- `ui_chronicle_panel.png` (256x384 or 9-slice)
- `ui_raid_panel.png` (256x384 or 9-slice)
- `ui_resource_icons/`
  - `icon_herb.png` (16x16)
  - `icon_ore.png` (16x16)
  - `icon_fish.png` (16x16)
  - `icon_wheat.png` (16x16)
  - `icon_wood.png` (16x16)
  - `icon_stone.png` (16x16)
  - `icon_gem.png` (16x16)

#### Items (16x16) — M6+
- `item_potion_health.png`
- `item_potion_strength.png`
- `item_potion_speed.png`
- `item_meal_stew.png`
- `item_meal_feast.png`
- `item_weapon_sword.png`
- `item_weapon_staff.png`
- `item_armor_vest.png`
- `item_armor_mail.png`
- `item_scroll_fire.png`
- `item_scroll_shield.png`

#### Effects — M1–M4
- `effect_damage.png` (8x8, red flash)
- `effect_death.png` (16x16, fade particle)

#### Effects — M5+
- `effect_level_up.png` (16x16, sparkle)

## 8. File Structure

Every release version of the game **must** include a `manual.md` at the repository root. This file documents controls, UI flow, and any gameplay mechanics specific to that version so players (and testers) can pick up the game without reading the full spec.

```
dungeon-keep/
├── SPEC.md                  # This document
├── manual.md                # Player-facing controls & gameplay guide (required per version)
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
├── npc.py                   # NPC data, personalities, guild management
├── professions.py           # Profession definitions, production ticks, leveling
├── crafting.py              # Recipes, resource inventory, crafting queue
├── raids.py                 # Raid party formation, auto-battle, loot tables
├── trading.py               # Auction house, market demand, visitors
├── village.py               # Multi-tile building placement, grid expansion, camera
├── codex.py                 # Progression tracking, completion %, milestone rewards
├── chronicle.py             # Event log, timestamps, summary generation
├── camera.py                # Camera system for scrolling (M5+)
└── assets/
    ├── tiles/
    │   ├── tile_stone_floor.png
    │   ├── tile_stone_wall.png
    │   ├── tile_dungeon_heart.png
    │   ├── tile_lair.png
    │   ├── tile_trap_room.png
    │   ├── tile_treasury.png
    │   ├── tile_farm.png
    │   ├── tile_alchemy_lab.png
    │   ├── tile_kitchen.png
    │   ├── tile_forge.png
    │   ├── tile_enchanting_table.png
    │   ├── tile_mine.png
    │   ├── tile_dock.png
    │   ├── tile_guild_hall.png
    │   └── tile_auction_house.png
    ├── units/
    │   ├── unit_goblin_idle.png
    │   ├── unit_slime_idle.png
    │   ├── unit_skeleton_idle.png
    │   ├── unit_hero_adventurer.png
    │   ├── unit_hero_knight.png
    │   ├── unit_hero_paladin.png
    │   └── npc_portraits/
    │       ├── npc_portrait_01.png through npc_portrait_30.png
    │       └── npc_visitor_01.png through npc_visitor_10.png
    ├── ui/
    │   ├── ui_panel.png
    │   ├── ui_button_default.png
    │   ├── ui_button_hover.png
    │   ├── ui_button_disabled.png
    │   ├── ui_gold_icon.png
    │   ├── ui_cursor_build.png
    │   ├── ui_cursor_select.png
    │   ├── ui_guild_panel.png
    │   ├── ui_crafting_panel.png
    │   ├── ui_auction_panel.png
    │   ├── ui_codex_panel.png
    │   ├── ui_chronicle_panel.png
    │   ├── ui_raid_panel.png
    │   └── ui_resource_icons/
    │       ├── icon_herb.png
    │       ├── icon_ore.png
    │       ├── icon_fish.png
    │       ├── icon_wheat.png
    │       ├── icon_wood.png
    │       ├── icon_stone.png
    │       └── icon_gem.png
    ├── items/
    │   ├── item_potion_health.png
    │   ├── item_potion_strength.png
    │   ├── item_meal_stew.png
    │   ├── item_weapon_sword.png
    │   ├── item_armor_vest.png
    │   └── item_scroll_fire.png
    └── effects/
        ├── effect_damage.png
        ├── effect_death.png
        └── effect_level_up.png
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

### 9.9 `npc.py`
```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class NPCStats:
    hp: int
    max_hp: int
    attack: int
    defense: int
    speed: float
    profession_bonus: float = 1.0

@dataclass
class NPC:
    id: int
    name: str
    portrait_id: str
    traits: List[str]
    profession: str
    morale: int
    level: int
    stats: NPCStats
    state: str  # 'idle', 'working', 'raiding', 'resting'
    profession_xp: int = 0
    rest_cooldown: float = 0.0

NPC_NAMES: List[str] = [...]  # Pool of 120 unique names
PERSONALITY_TRAITS: List[str] = [...]  # Pool of 20 traits

class GuildManager:
    def __init__(self, max_members: int = 12) -> None: ...
    def add_member(self, npc: NPC) -> bool: ...
    def remove_member(self, npc_id: int) -> None: ...
    def get_member(self, npc_id: int) -> Optional[NPC]: ...
    def get_all_members(self) -> List[NPC]: ...
    def assign_profession(self, npc_id: int, profession: str) -> bool: ...
    def update_morale(self, npc_id: int, delta: int) -> None: ...
    def update_all(self, dt: float) -> None: ...
    def roll_recruitment(self, hero_type: str) -> Optional[NPC]: ...
    @property
    def member_count(self) -> int: ...
```

### 9.10 `professions.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class ProfessionDef:
    name: str
    building_required: str
    output_resources: List[Tuple[str, int]]  # (resource_name, amount)
    base_rate: float  # seconds per production tick
    xp_per_tick: int

PROFESSIONS: Dict[str, ProfessionDef] = {...}

class ProfessionSystem:
    def __init__(self) -> None: ...
    def tick_production(self, npc: NPC, dt: float, buildings: dict) -> List[Tuple[str, int]]: ...
    def gain_xp(self, npc: NPC, amount: int) -> bool: ...  # returns True if leveled up
    def get_profession_level(self, npc: NPC) -> int: ...
    def can_assign(self, npc: NPC, profession: str, buildings: dict) -> bool: ...
```

### 9.11 `crafting.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto

class Quality(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()

@dataclass
class Recipe:
    id: str
    name: str
    category: str
    resources: Dict[str, int]  # resource_name -> amount needed
    profession: str
    min_profession_level: int
    craft_time: float  # seconds
    quality_weights: Dict[Quality, float]

@dataclass
class CraftItem:
    recipe_id: str
    name: str
    quality: Quality
    stats: Dict[str, int]  # e.g., {'heal': 20} or {'attack': 5}

@dataclass
class CraftJob:
    recipe: Recipe
    assigned_npc_id: int
    time_remaining: float

RECIPES: Dict[str, Recipe] = {...}

class CraftingSystem:
    def __init__(self) -> None: ...
    def get_resources(self) -> Dict[str, int]: ...
    def add_resource(self, name: str, amount: int) -> None: ...
    def remove_resources(self, costs: Dict[str, int]) -> bool: ...
    def can_craft(self, recipe_id: str, npc: NPC) -> bool: ...
    def start_craft(self, recipe_id: str, npc_id: int) -> bool: ...
    def update(self, dt: float) -> List[CraftItem]: ...  # returns newly completed items
    def get_inventory(self) -> List[CraftItem]: ...
    def equip_item(self, npc_id: int, item: CraftItem) -> bool: ...
```

### 9.12 `raids.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class DungeonFloor:
    floor_number: int
    monster_type: str
    monster_count: int
    monster_stats: Dict[str, int]

@dataclass
class Dungeon:
    id: str
    name: str
    floors: List[DungeonFloor]
    min_party_level: int
    reward_table: List[Tuple[str, int, float]]  # (item_id, amount, drop_chance)

@dataclass
class RaidResult:
    dungeon_id: str
    floors_cleared: int
    loot: List[CraftItem]
    xp_gained: Dict[int, int]  # npc_id -> xp
    casualties: List[int]  # npc_ids that quit
    duration: float

DUNGEONS: Dict[str, Dungeon] = {...}

class RaidSystem:
    def __init__(self) -> None: ...
    def form_party(self, npc_ids: List[int]) -> bool: ...
    def can_raid(self, dungeon_id: str, party: List[NPC]) -> bool: ...
    def start_raid(self, dungeon_id: str) -> None: ...
    def update(self, dt: float) -> Optional[RaidResult]: ...  # returns result when raid completes
    @property
    def raid_in_progress(self) -> bool: ...
    @property
    def raid_progress(self) -> float: ...  # 0.0 to 1.0
```

### 9.13 `trading.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto

class Demand(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()

@dataclass
class MarketListing:
    item: CraftItem
    price: int
    seller_is_player: bool

@dataclass
class Visitor:
    id: int
    name: str
    wanted_items: List[str]  # item categories they buy
    budget: int
    time_remaining: float

class TradingSystem:
    def __init__(self) -> None: ...
    def get_demand(self, category: str) -> Demand: ...
    def list_item(self, item: CraftItem, price: int) -> bool: ...
    def unlist_item(self, listing_id: int) -> None: ...
    def update(self, dt: float) -> List[Tuple[str, int]]: ...  # returns sales (item_name, gold)
    def spawn_visitor(self) -> Optional[Visitor]: ...
    def get_bargain_items(self) -> List[MarketListing]: ...
    def buy_bargain(self, listing_id: int) -> Optional[CraftItem]: ...
    def get_sales_log(self) -> List[Tuple[str, int, float]]: ...  # (item_name, gold, timestamp)
```

### 9.14 `village.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class BuildingDef:
    name: str
    width: int
    height: int
    cost: int
    tile_type: str
    unlock_milestone: int

BUILDINGS: Dict[str, BuildingDef] = {...}

@dataclass
class PlacedBuilding:
    id: int
    name: str
    grid_x: int
    grid_y: int
    width: int
    height: int

class VillageSystem:
    def __init__(self, grid: 'Grid') -> None: ...
    def can_place(self, building_name: str, gx: int, gy: int) -> bool: ...
    def place_building(self, building_name: str, gx: int, gy: int) -> Optional[PlacedBuilding]: ...
    def remove_building(self, building_id: int) -> None: ...
    def get_buildings(self) -> List[PlacedBuilding]: ...
    def get_building_at(self, gx: int, gy: int) -> Optional[PlacedBuilding]: ...
    def expand_grid(self, new_width: int, new_height: int) -> None: ...
    def has_building_type(self, building_name: str) -> bool: ...
```

### 9.15 `codex.py`
```python
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class CodexEntry:
    category: str
    item_id: str
    name: str
    discovered: bool = False

@dataclass
class CodexCategory:
    name: str
    entries: List[CodexEntry]
    milestone_rewards: Dict[int, str]  # percent -> reward description

class CodexSystem:
    def __init__(self) -> None: ...
    def discover(self, category: str, item_id: str) -> bool: ...  # returns True if new
    def get_completion(self, category: str) -> Tuple[int, int]: ...  # (discovered, total)
    def get_total_completion(self) -> float: ...  # 0.0 to 1.0
    def check_milestones(self, category: str) -> List[str]: ...  # returns newly hit milestones
    def get_all_categories(self) -> Dict[str, CodexCategory]: ...
```

### 9.16 `chronicle.py`
```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ChronicleEntry:
    timestamp: float  # game time in seconds
    wave_number: int
    event_type: str
    description: str

class Chronicle:
    def __init__(self) -> None: ...
    def log(self, event_type: str, description: str, wave: int, game_time: float) -> None: ...
    def get_entries(self, limit: int = 50) -> List[ChronicleEntry]: ...
    def get_summary(self) -> Dict[str, int]: ...  # event_type -> count
    def get_highlights(self) -> List[ChronicleEntry]: ...  # major events only
```

### 9.17 `camera.py`
```python
class Camera:
    def __init__(self, viewport_width: int, viewport_height: int) -> None: ...
    def update(self, target_x: float, target_y: float) -> None: ...
    def set_position(self, x: float, y: float) -> None: ...
    @property
    def offset_x(self) -> int: ...
    @property
    def offset_y(self) -> int: ...
    def screen_to_world(self, sx: int, sy: int) -> Tuple[int, int]: ...
    def world_to_screen(self, wx: int, wy: int) -> Tuple[int, int]: ...
    def clamp(self, world_width: int, world_height: int) -> None: ...
```

## 10. Milestones & Acceptance Criteria (Refined Vision)

> **Design basis:** `DESIGN_VISION.md` — Evil Hunter Tycoon × Dungeon Maker × Creator Chronicles

---

### Milestone 1: Skeleton (Architecture & Rendering) ✅ COMPLETE
**Goal:** A running window with a grid, clickable tiles, and placeholder colored rectangles.

**AC:**
- [x] Window opens at 768x384 (scaled to 1536x768)
- [x] 16x12 grid renders with distinct colors for floor and wall
- [x] Dungeon Heart placed at center
- [x] Left-clicking a tile logs its coordinates
- [x] Game loop runs at stable 60 FPS
- [x] Title screen → Game screen transition works
- [x] `assets/` directory exists with placeholder PNGs (colored squares)

**Est. Effort:** Senior Dev — 1 session

---

### Milestone 2: Room-Based Defense (Dungeon Maker Core)
**Goal:** Monsters are stationary in Battle Rooms; heroes walk a gauntlet from fixed Entrance to Dungeon Heart.

**AC:**
- [ ] Add `ENTRANCE` tile (left edge, fixed spawn point for heroes)
- [ ] Heroes path Entrance → Dungeon Heart in a linear corridor
- [ ] Rename `LAIR` to `BATTLE_ROOM`; monsters are assigned to rooms (1–3 per room)
- [ ] Monsters do NOT move; they attack heroes who enter their tile
- [ ] If all monsters in a Battle Room die, room is "overrun" — heroes walk through
- [ ] Trap Rooms trigger when hero **walks onto** the trap tile (not adjacent)
- [ ] Heroes move tile-by-tile at fixed speed (already implemented)
- [ ] Win/Loss: Dungeon Heart has HP; reaching 0 = loss. Survive all nights = win.

**Est. Effort:** Senior Dev — 1–2 sessions | Designer — room sprites, entrance sprite

---

### Milestone 3: Day/Night Cycle
**Goal:** Explicit Day (build) → Night (defend) → Dawn (recover) loop.

**AC:**
- [ ] Day timer (e.g., 60s) — building, recruiting, assignment allowed
- [ ] Dusk warning (5s countdown) — UI shows "Night Approaches"
- [ ] Night timer (e.g., 90s) — heroes spawn from Entrance and march; building locked
- [ ] Dawn phase — collect gold from hero kills, monsters heal, UI shows night summary
- [ ] Difficulty scales per night (more heroes, stronger heroes, new hero types)
- [ ] Pause works in both Day and Night (spacebar)
- [ ] Night summary overlay: heroes killed, gold earned, rooms lost, monsters died

**Est. Effort:** Senior Dev — 1–2 sessions | Designer — day/night UI, timer visuals

---

### Milestone 4: Guild Members & Facilities (Evil Hunter Tycoon Core)
**Goal:** NPC workers staff Facilities; have traits, professions, stress, and morale.

**AC:**
- [ ] Facility rooms: `KITCHEN`, `FORGE`, `ALCHEMY_LAB`, `INFIRMARY`, `TAVERN`, `TRADING_POST`
- [ ] Guild Member data model: name, portrait_id, 2 traits, profession, morale (0–100), stress (0–100)
- [ ] Pool of 30+ NPC names and 20 personality traits
- [ ] Wandering NPCs appear at Entrance during Day; click to recruit (pay gold)
- [ ] Assign guild member to a Facility (drag-and-drop or click-to-assign)
- [ ] Passive production during Day based on profession + facility match
- [ ] Stress system: rises when monsters die / night is failed; falls when Tavern is staffed / day off given
- [ ] If stress reaches 100, NPC quits permanently
- [ ] Guild panel UI: list members, portraits, traits, morale/stress bars, assign profession

**Est. Effort:** Senior Dev — 2 sessions | Designer — NPC portraits, facility sprites, guild panel UI

---

### Milestone 5: Crafting & Trading
**Goal:** Resources are produced, recipes are crafted, and items are sold to merchants.

**AC:**
- [ ] Resource inventory: Herbs, Ore, Meat, Mana Dust
- [ ] Facilities produce resources passively when staffed (e.g., Kitchen → Meat, Forge → Ore)
- [ ] Recipe system: 10+ recipes (potions, meals, weapons, armor)
- [ ] Crafting panel UI: recipe list, resource counts, "Craft" button
- [ ] Crafted items go to inventory; can be equipped on monsters or sold
- [ ] Trading Post: Merchants visit during Day with randomized buy requests
- [ ] Merchant UI: "I need 3 Health Potions — 50g each" → Accept / Decline / Haggle
- [ ] Haggle mini-game: guess merchant's max price (3 tries)

**Est. Effort:** Senior Dev — 2 sessions | Designer — resource icons, crafting UI, merchant portraits

---

### Milestone 6: Equipment & Monster Progression
**Goal:** Monsters equip crafted gear; rooms upgrade; Codex tracks progression.

**AC:**
- [ ] Monsters can equip 1 weapon (+damage) and 1 armor (+HP)
- [ ] Equipment is lost if monster dies in combat
- [ ] Battle Rooms can be upgraded with gold (+1 monster slot, +stat buffs)
- [ ] New monster types unlocked via Codex progression (Imp, Golem)
- [ ] Codex panel: 6 categories (Monsters, Rooms, Recipes, Heroes, Guild, Dungeons)
- [ ] Milestone rewards at 25/50/75/100% per category (unlock new content)
- [ ] Win/Loss screen shows Codex progress + night summary

**Est. Effort:** Senior Dev — 2 sessions | Designer — equipment icons, codex UI

---

### Milestone 7: Hero Parties & Advanced Rooms
**Goal:** Heroes arrive in synergistic parties; special rooms add strategic depth.

**AC:**
- [ ] Hero parties: Tank (front), DPS (middle), Healer (back)
- [ ] Tank absorbs trap damage; Healer heals party; DPS deals damage to monsters
- [ ] Special Battle Rooms: `ARENA` (+ATK), `BLOOD_ALTAR` (vampirism), `BARRIER` (+DEF)
- [ ] Special Trap Rooms: `CURSE_TRAP` (weaken), `ICE_TRAP` (slow), `POISON_TRAP` (DoT)
- [ ] Room synergy: e.g., Slow trap + Arena = kill tank before DPS arrives
- [ ] Infirmary can "save" a dying monster (50% chance) if staffed
- [ ] 10 nights total, each with escalating difficulty

**Est. Effort:** Senior Dev — 2 sessions | Designer — special room sprites, hero class sprites

---

### Milestone 8: Polish, Art Pass & Browser Build
**Goal:** Final art, sound, balance, and pygbag browser build.

**AC:**
- [ ] All placeholder art replaced with final pixel art (Dungeon Settler style)
- [ ] Sound effects: trap trigger, monster attack, hero death, gold jingle, UI click
- [ ] Music: ambient day theme, tense night theme
- [ ] Death animations for heroes and monsters
- [ ] Particle effects: trap sparks, level-up sparkle, gold pop
- [ ] Balance pass: economy feels tight but fair; nights 1–3 are tutorial; nights 8–10 are hard
- [ ] `pygbag` builds successfully and runs in browser
- [ ] `manual.md` updated for final controls and mechanics
- [ ] Full loop playable in 15–20 minutes: Build → Recruit → Craft → Defend → Progress

**Est. Effort:** Senior Dev — 2 sessions | Designer — final asset pass, sound design

---

### Milestone 9+: Post-Prototype Expansion (Optional)
- Save/load system
- Endless mode (survive infinite nights)
- Dungeon raids (send monsters to attack hero towns)
- Multi-tile buildings and camera scrolling
- Steam release prep

---

## 11. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| A* pathfinding too slow on grid | Low | Medium | Grid is only 16x12 (24x18 from M5); precalculate if needed |
| Pygbag WASM build fails | Medium | High | Test build at M1; keep dependencies minimal |
| Art delivery delayed | Medium | Medium | Use colored rectangles as drop-in replacements |
| Scope creep (multi-tile rooms, tech tree) | High | High | PM gate; update SPEC.md via PR only |
| Frame drops with many entities | Low | Medium | Cap max monsters/heroes; pool entities |
| NPC system too complex for prototype | Medium | High | Start with 30 NPCs max; simplify traits to 2 per NPC |
| Camera scrolling breaks input mapping | Medium | Medium | Implement camera.py early in M5; test input thoroughly |
| Crafting balance (economy too fast/slow) | High | Medium | PM reviews production rates at M6 milestone gate |
| Raid auto-battle feels unsatisfying | Medium | Medium | Add battle log detail; allow manual intervention in future |
| Save/load needed for full experience | High | High | Defer to post-prototype; use session-only state for M1–M8 |

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
| 2026-09-24 | 0.2.0 | PM | Major expansion: Added NPC/Guild system, Professions, Crafting, Dungeon Raids, Trading/Auction House, Village Expansion (multi-tile), Codex, Chronicle. New milestones M5–M8. New modules: npc.py, professions.py, crafting.py, raids.py, trading.py, village.py, codex.py, chronicle.py, camera.py |
| 2026-09-25 | 0.3.0 | PM | **Design Pivot**: Merged Evil Hunter Tycoon (town management) + Dungeon Maker (room-based defense) + Creator Chronicles (guild sim & stress). Rewrote milestones M2–M8. Added `DESIGN_VISION.md`. Core shift: stationary monsters in Battle Rooms, fixed Entrance gauntlet, Day/Night cycle, Guild Members staff Facilities, Crafting & Trading economy. Removed free-roaming monsters, random-edge spawning, and multi-tile buildings from prototype scope. |

---
*This SPEC is the source of truth. Any deviation requires a PR with PM approval.*
