# Dungeon Keep — Refined Design Vision

> **Influences:** Evil Hunter Tycoon (town management loop) + Dungeon Maker (room-based defense) + Creator Chronicles (guild sim & mental health) + Dungeon Settler (pixel art aesthetic)
> **Date:** 2026-09-25

---

## 1. Elevator Pitch

You are the **Dungeon Keeper**. Not a hero. Not a monster. The *manager*.

During the **Day**, you build rooms, recruit monsters, hire guild members, craft gear, and trade with wandering merchants. During the **Night**, heroes invade through a fixed entrance and march toward your Dungeon Heart. Your monsters defend their assigned rooms automatically. You watch, adapt, and survive until dawn.

The loop is **management-first, action-second** — like Evil Hunter Tycoon meets Dungeon Maker. You don't click to attack. You design the dungeon that does the attacking for you.

---

## 2. Core Loop (The Day/Night Cycle)

```
┌─────────────────────────────────────────────────────────────┐
│  DAWN (Build Phase)                                         │
│  ├── Build / upgrade rooms                                  │
│  ├── Recruit monsters & assign to Battle Rooms              │
│  ├── Hire guild members & assign to Facilities              │
│  ├── Craft equipment, potions, meals                        │
│  ├── Trade with merchants at the Trading Post               │
│  └── Equip monsters with crafted gear                       │
│                         ↓                                   │
│  DUSK → NIGHT (Defense Phase)                               │
│  ├── Heroes enter from the dungeon entrance (left side)     │
│  ├── Heroes path toward the Dungeon Heart (right side)      │
│  ├── Traps trigger as heroes walk over them                 │
│  ├── Monsters in Battle Rooms attack automatically          │
│  └── Combat resolves in real-time (with pause)              │
│                         ↓                                   │
│  DAWN (Recovery Phase)                                      │
│  ├── Collect loot & gold from defeated heroes               │
│  ├── Monsters heal at Infirmary (if built)                  │
│  ├── Guild members produce resources at their stations      │
│  ├── Check morale / stress levels                           │
│  └── Prepare for the next night                             │
└─────────────────────────────────────────────────────────────┘
```

**Day/Night is explicit.** A timer counts down (e.g., 60s of Day, 90s of Night). The player knows exactly when the invasion starts.

---

## 3. Room System (Dungeon Maker DNA)

Rooms are the atomic unit of design. Every room occupies **1 tile** and has a purpose.

### 3.1 Room Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Battle Room** | Holds monsters; monsters defend this room and do NOT leave it | Goblin Barracks, Skeleton Crypt |
| **Trap Room** | Damages or debuffs heroes who step on it | Spike Trap, Fire Trap, Curse Trap |
| **Facility** | Supports the dungeon economy; staffed by guild members | Kitchen, Forge, Infirmary, Tavern, Trading Post |
| **Core** | Required for game function | Dungeon Heart, Entrance |
| **Lair** | Recruits monsters (special Facility) | Monster Lair |

### 3.2 Battle Rooms (The Front Line)

- Each Battle Room holds **1–3 monsters** (depending on room level)
- Monsters are **stationary** — they do not chase heroes. They attack heroes in their room.
- If a hero enters a Battle Room, combat starts automatically
- If all monsters in a room die, the room is "overrun" — heroes pass through freely
- **Room Level:** Battle Rooms can be upgraded with gold to hold more monsters or grant stat buffs

**Monster AI in Battle Rooms:**
```
if hero in same room:
    attack hero (cooldown based)
else:
    idle (no movement)
```

This is a **massive simplification** from the current free-roaming monsters and is key to the Dungeon Maker feel.

### 3.3 Trap Rooms

- Placed on floor tiles that heroes will walk over
- Trigger when a hero **enters** the trap tile
- Effects: damage, slow, blind, poison, weaken
- **Charge system** (from Dungeon Maker v1.8+): Some traps recharge over time and trigger again
- Can be dodged by heroes with "Dodge Trap" buff (rare)

### 3.4 Facilities (Evil Hunter Tycoon DNA)

Facilities are staffed by **Guild Members** during the Day phase.

| Facility | Function | Staffed By |
|----------|----------|------------|
| **Kitchen** | Produces meals; meals boost monster stats for one night | Cook |
| **Forge** | Crafts weapons & armor for monsters | Blacksmith |
| **Alchemy Lab** | Brews potions (healing, strength, speed) | Alchemist |
| **Infirmary** | Heals wounded monsters between nights | Healer / Nurse |
| **Tavern** | Reduces guild member & monster stress; boosts morale | Bartender |
| **Trading Post** | Sell crafted items to visiting merchants | Merchant |
| **Treasury** | Generates +1 gold/sec | (passive) |
| **Lair** | Recruit new monsters | (click to recruit) |

**Facility Level:** Upgrading a facility increases production speed and unlocks higher-tier recipes.

---

## 4. Heroes & Invasion Path

### 4.1 Invasion Path

Heroes enter from a fixed **Entrance** tile (left side of map) and path toward the **Dungeon Heart** (right side). The path is a corridor the player designs by placing rooms.

```
[ENTRANCE] → [Trap] → [Battle Room] → [Trap] → [Battle Room] → [DUNGEON HEART]
```

This is **not** an open field. It's a **gauntlet** the player designs.

### 4.2 Hero Behavior

- Heroes move **tile by tile** at fixed speed (already implemented)
- They walk through Trap Rooms (taking damage)
- They stop in Battle Rooms to fight monsters
- If a Battle Room is empty, they walk through it
- If they reach the Dungeon Heart, they damage it
- **Dungeon Heart HP:** If it reaches 0, game over

### 4.3 Hero Parties

Instead of random individual heroes, heroes arrive in **parties**:
- Tank (high HP, low damage) — walks first, absorbs trap damage
- DPS (medium HP, high damage) — walks behind tank
- Healer (low HP, heals party) — walks at the back

This makes room synergy matter (e.g., a Slow trap helps your Battle Room monsters kill the tank before the DPS arrives).

---

## 5. Guild Member System (Creator Chronicles DNA)

### 5.1 What Are Guild Members?

Guild members are **NPC workers** who staff your Facilities. They are NOT combat units (that's what monsters are for). They are the "hunters" from Evil Hunter Tycoon — but in reverse. Instead of hiring heroes to fight for you, you hire monsters to defend and guild members to support.

### 5.2 Recruitment

- **Between nights**, wandering NPCs appear at the dungeon entrance
- Click them to see their stats, traits, and profession
- Pay gold to hire them
- If you decline, they walk away

### 5.3 Professions & Assignment

Each guild member has a **primary profession**. They can only work in matching facilities.

| Profession | Works In | Passively Produces |
|------------|----------|-------------------|
| Cook | Kitchen | Meals (boost monster stats) |
| Blacksmith | Forge | Weapons, Armor |
| Alchemist | Alchemy Lab | Potions |
| Healer | Infirmary | Heals monsters over time |
| Merchant | Trading Post | Better trade prices |

### 5.4 Traits & Personality (Creator Chronicles DNA)

Each NPC has **2 traits** from a pool of 20:

| Trait | Effect |
|-------|--------|
| Hardworking | +20% production speed |
| Lazy | -20% production speed |
| Optimist | +10 morale, +5% party morale |
| Pessimist | -10 morale, -5% party morale |
| Greedy | Costs +50% gold to hire, but produces +10% value |
| Loyal | Never quits from low morale |
| Fragile | -50% stress threshold (quits easily) |
| Brave | +10% combat boost to assigned monsters |
| Social | +5 morale to all workers in same facility |
| Loner | +15% production when alone in facility |

### 5.5 Morale & Stress (The Creator Chronicles Twist)

**Stress** (0–100) goes UP when:
- A night is failed (heroes reach the Heart)
- A guild member is overworked (no rest between nights)
- Monsters die in Battle Rooms

**Stress** goes DOWN when:
- A night is survived perfectly
- Tavern is built and staffed
- Guild member is given a day off (not assigned to work)

**If stress reaches 100:** The guild member **quits permanently** (like Creator Chronicles' "glass-hearted" members).

**If morale drops below 30:** Production speed halved.

---

## 6. Monster System

### 6.1 Recruitment

- Click a **Lair** → pay gold → monster is added to your "bench"
- Monsters on the bench do nothing until assigned to a **Battle Room**

### 6.2 Assignment

- Click a Battle Room → see empty slots → drag a benched monster into the slot
- Monsters are **locked to that room** until the night ends or they die

### 6.3 Equipment

- Monsters can equip **1 weapon** and **1 armor** crafted by the Blacksmith
- Weapons: +damage
- Armor: +HP
- Equipment is consumed if the monster dies (lost forever)

### 6.4 Monster Types

| Monster | HP | DMG | ATK Spd | Room Bonus | Cost |
|---------|----|-----|---------|------------|------|
| Goblin | 30 | 5 | 1.0/s | +1 gold per kill | 20g |
| Slime | 50 | 3 | 0.8/s | Slows heroes by 20% | 15g |
| Skeleton | 40 | 8 | 0.6/s | +50% damage vs. Paladins | 30g |
| Imp | 25 | 4 | 1.5/s | Sets heroes on fire (DoT) | 25g |
| Golem | 100 | 6 | 0.5/s | Tank — takes 50% less trap damage | 50g |

### 6.5 Monster Death

- If a monster dies in combat, it is **removed from the bench** permanently
- This makes equipment loss sting and creates tension
- **Infirmary** can "save" a dying monster if built and staffed (50% chance)

---

## 7. Crafting & Economy

### 7.1 Resources

Produced passively by staffed Facilities during the Day:

| Resource | Produced By | Used For |
|----------|-------------|----------|
| Herbs | Alchemy Lab | Potions |
| Ore | Forge | Weapons, Armor |
| Meat | Kitchen | Meals |
| Mana Dust | Alchemy Lab | Scrolls, Enchantments |

### 7.2 Recipes

| Item | Facility | Resources | Effect |
|------|----------|-----------|--------|
| Health Potion | Alchemy Lab | 2 Herbs | Heals monster +20 HP |
| Strength Elixir | Alchemy Lab | 3 Herbs + 1 Mana Dust | Monster +5 damage for 1 night |
| Iron Sword | Forge | 2 Ore | Monster +3 damage |
| Steel Armor | Forge | 3 Ore | Monster +15 HP |
| Hearty Stew | Kitchen | 2 Meat | All monsters +10 HP for 1 night |
| Speed Pie | Kitchen | 2 Meat + 1 Herb | All monsters +20% attack speed |

### 7.3 Trading

- A **Trading Post** facility (staffed by Merchant) allows selling items
- **Merchants** appear during the Day with randomized wants
- "I need 3 Health Potions — will pay 50g each"
- Player can accept, decline, or haggle (mini-game: guess the merchant's max price)

---

## 8. The Codex (Progression)

Tracks everything the player has discovered. Categories:

| Category | Tracks | Reward at Milestones |
|----------|--------|---------------------|
| Monsters | Monsters recruited | Unlock rare monster types |
| Rooms | Rooms built | Unlock special room types |
| Recipes | Items crafted | Unlock higher-tier recipes |
| Heroes | Hero types defeated | Unlock intel on hero weaknesses |
| Guild | Members recruited | Increase max member cap |
| Dungeons | Raids completed | Unlock harder raids |

---

## 9. Art Direction

**Style:** Dungeon Settler — dark fantasy pixel art with a cozy, "lived-in" feel.

- **Palette:** Muted earth tones with pops of magical glow (purple heart, gold UI, green slime)
- **Tiles:** 32×32, hand-drawn pixel art, not AI-generated
- **Characters:** Chunky, readable silhouettes. 2-frame idle animations.
- **UI:** Stone-and-wood aesthetic. No neon. No gradients.
- **Lighting:** The dungeon should feel dimly lit. Torches, heart glow, and trap fires provide warm light sources.

---

## 10. What's Different from the Current Build?

| Current | Refined Vision |
|---------|---------------|
| Monsters roam freely and chase heroes | Monsters are **stationary** in Battle Rooms |
| Heroes spawn at random edges | Heroes enter from a **fixed Entrance** and walk a gauntlet |
| Economy = Treasury passive income | Economy = **Facility production + Trading + Kills** |
| No guild members | **Guild members** staff facilities, have traits, stress, morale |
| No day/night cycle | Explicit **Day/Night cycle** with build → defend phases |
| Traps damage adjacent tiles | Traps trigger when **walked on** |
| Win/Loss after 3 waves | Survive **X nights**, each harder than the last |
| No crafting | **Full crafting** system with recipes and resources |
| No equipment | Monsters equip **crafted gear** |

---

## 11. Implementation Priority

This is a big pivot. Here's the order to implement without breaking the current codebase:

### Phase 1: Room-Based Defense (Dungeon Maker Core)
1. Change monster AI: stationary in rooms, attack heroes in same room
2. Add Entrance tile (fixed spawn point)
3. Heroes path Entrance → Heart (linear gauntlet)
4. Traps trigger on walk-over, not adjacent

### Phase 2: Day/Night Cycle
1. Add Day timer (build phase)
2. Add Night timer (defense phase)
3. Lock building during Night
4. Add Dawn recovery phase (heal, collect loot)

### Phase 3: Guild Members & Facilities
1. Add Facility rooms (Kitchen, Forge, etc.)
2. Add Guild Member system (recruit, traits, professions)
3. Add assignment UI (drag member to facility)
4. Add passive production during Day

### Phase 4: Crafting & Trading
1. Add resource inventory
2. Add recipe system
3. Add crafting queue
4. Add Trading Post and merchant visits

### Phase 5: Equipment & Progression
1. Monsters can equip crafted items
2. Add Codex tracking
3. Add room upgrades
4. Add special room unlocks

---

## 12. One-Sentence Summary

> **Dungeon Keep** is a dungeon-management tycoon where you build a gauntlet of battle rooms and traps, staff facilities with quirky guild members who craft gear for your monsters, and survive increasingly difficult hero invasions every night — all in a cozy-but-deadly pixel art dungeon.
