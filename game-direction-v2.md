New core fantasy

“Build a living dungeon. Recruit monsters. Set up defenses. Then watch adventurers invade and try to survive your dungeon.”

The player shouldn't spend most of their time controlling individual units. Their decisions happen before and between invasions, while combat itself is mostly autonomous.

Core gameplay loop

1. Expand the dungeon
→ dig rooms
→ connect corridors
→ place traps
→ build monster habitats
→ unlock deeper floors

2. Recruit monsters
→ Slime
→ Goblin
→ Skeleton
→ Orc
→ Spider
→ Shaman
→ etc.

Each monster has a job inside the dungeon, not just combat stats.

3. Prepare the defense

For example:

              ENTRANCE
                 ↓
        ┌─────────────────┐
        │   Spike Trap    │
        └────────┬────────┘
                 ↓
      ┌─────────────────────┐
      │   Goblin Ambush     │
      │  👺          👺     │
      └──────────┬──────────┘
                 ↓
        ┌─────────────────┐
        │   Slime Pool    │
        │    🟢 🟢 🟢     │
        └────────┬────────┘
                 ↓
      ┌─────────────────────┐
      │    Skeleton Hall    │
      │ ☠️ ☠️ ☠️ ☠️        │
      └──────────┬──────────┘
                 ↓
             TREASURE
                 ↓
             CORE ROOM

4. Press “Defend”

Adventurers enter.

And then...

⚔️ AUTO COMBAT

The dungeon fights automatically.

You watch the invasion unfold:

        HUMAN INVADERS

   ⚔️ Knight      🏹 Archer
          \        /
           \      /
            ↓    ↓

       👺 Goblin 👺
          ⚔️  ⚔️

      🟢 Slime Pool
       💥  💥  💥

       ☠️ Skeleton
          ↓
       💀 CRUSHED

Your interaction during combat should be limited but meaningful, rather than traditional RTS micro.

For example:

activate dungeon trap
spend mana to buff a monster
close/open a door
trigger an emergency ability
sacrifice a monster
summon reinforcements

So the player watches the strategy they designed being tested.

The really important part: make the dungeon itself the “character”

This is where I think the game can become much more interesting.

Instead of:

“I have 10 monsters.”

Make the player think:

“I built a dungeon that turns adventurers into food.”

Your dungeon has synergies.

For example:

Goblin Den

Goblin gets bonuses when fighting in its own habitat.

Slime Pool

Slimes slow enemies.

Skeleton Crypt

Skeletons respawn after dying.

Spider Nest

Spiders web enemies.

Orc Barracks

Orcs become stronger when another monster dies nearby.

Now you can create combinations:

SPIDER NEST
     ↓
Web enemy
     ↓
SLIME POOL
     ↓
Slow enemy
     ↓
GOBLIN AMBUSH
     ↓
Attack weakened enemy
     ↓
SKELETON CRYPT
     ↓
Finish survivors

The fun becomes designing a machine that destroys adventurers automatically.

Adventurers should be your roguelike “content”

This is another big opportunity.

Don't make humans generic HP bags.

Every invasion party has a composition.

Party A — Beginner Adventurers
⚔️ Knight
🏹 Archer
🧙 Apprentice

Easy invasion.

Party B — Goblin Hunters
⚔️ Paladin
🏹 Ranger
🔥 Fire Mage

Specifically dangerous to your goblins.

Party C — Treasure Hunters
⚔️ Fighter
🗡️ Rogue
🧙 Mage
💚 Healer

The healer changes the entire fight.

Party D — Dungeon Raid
⚔️⚔️ Knight
🏹🏹 Ranger
🧙 Mage
✝️ Priest

Much harder.

Eventually:

Boss invasion
             HERO PARTY

        ⚔️ Legendary Knight
                 |
       🧙 Archmage — ✝️ Priest
                 |
          🏹 Master Ranger

And your dungeon has to survive.

The progression loop

I'd structure the game around Depth.

                    DUNGEON CORE
                         │
                ┌────────┴────────┐
                │                 │
             FLOOR 1           FLOOR 2
                │                 │
          Goblins/Slimes     Skeletons/Spiders
                                  │
                              FLOOR 3
                                  │
                            Orcs/Shamans
                                  │
                              FLOOR 4
                                  │
                           Elite Monsters
                                  │
                              FLOOR 5
                                  │
                           DUNGEON LORD

Every time you survive enough invasions, you go deeper.

Deeper floors give:

stronger monsters
new rooms
new traps
new dungeon mechanics
better loot
harder adventurers

But also create more complicated defenses.

Monster progression

Instead of simply:

Goblin → Goblin II → Goblin III

I'd make monsters have evolution paths.

For example:

             Goblin
                │
        ┌───────┴────────┐
        ↓                ↓
     Goblin           Goblin
     Warrior          Shaman
        │                │
        ↓                ↓
    Hobgoblin       Witch Doctor

And:

Slime
  │
  ├── Acid Slime
  │
  ├── Ice Slime
  │
  └── Giant Slime

That gives players reasons to experiment.

Dungeon Settler art direction

For the visual style, I would not make it dark, gritty, realistic dungeon art.

Your reference direction should be closer to:

cute pixel-art settlement + miniature diorama + dungeon fantasy.

Think:

chunky pixel characters
readable silhouettes
exaggerated animations
cozy dungeon rooms
little monster idle animations
tiny environmental details
warm torchlight
humorous adventurer deaths
monsters having personalities

The contrast is important.

Your dungeon is basically:

a cozy monster village that happens to murder adventurers.

That gives the game a much stronger identity.

The UI should reinforce the fantasy

Instead of a conventional strategy-game UI:

HP
GOLD
WOOD
FOOD
BUILD
RESEARCH

I'd make the player feel like the Dungeon Master.

Something like:

┌────────────────────────────────────────────┐
│ 💎  Dungeon Core: Lv. 7     👑 DM         │
│                                            │
│  🪙 1,240      🔮 85 Mana     ☠️ 3 Souls  │
└────────────────────────────────────────────┘


             YOUR DUNGEON

       ┌─────────────────────┐
       │ 🟢 Slime Habitat    │
       │                     │
       │   🟢   🟢   🟢      │
       └──────────┬──────────┘
                  │
       ┌──────────▼──────────┐
       │ 👺 Goblin Barracks  │
       │   👺  👺  👺        │
       └──────────┬──────────┘
                  │
               ENTRANCE
                  │
             ⚔️⚔️⚔️
          "INVASION!"

Then the invasion begins.

The most important design rule

I would make the game approximately:

60% dungeon building / 20% monster management / 20% watching + reacting to battles

rather than:

80% clicking units during combat.

That gives you the Dungeon Master fantasy.

The player should feel clever when the invasion fails because:

“They walked exactly where I wanted them to.”

rather than:

“I clicked my knight 47 times.”

And I would change the prototype around this immediately

Your first playable vertical slice only needs:

Monsters
🟢 Slime
👺 Goblin
☠️ Skeleton
🛡️ Orc
Rooms
Slime Pool
Goblin Den
Skeleton Crypt
Treasure Room
Dungeon Core
Traps
Spike
Pit
Fire
Humans
Knight
Archer
Mage
Healer
One loop

Build → Recruit → Arrange → Start Invasion → Auto Battle → Loot → Upgrade → Repeat

That's enough to determine whether the game is actually fun before we build 30 monsters and 50 rooms.

And importantly, the dungeon layout itself should be part of the strategy, not just decoration. That is the piece that can make Dungeon Keep feel substantially different from a generic idle/auto-battler.






Dungeon Keep — MVP
👺 Monsters — only 3
Monster	Role	Simple ability
🟢 Slime	Tank / slow	Slows enemies
👺 Goblin	Basic DPS	Attacks quickly
☠️ Skeleton	Durable DPS	Revives once

No evolution, classes, equipment, rarity, or skill trees yet.

⚔️ Heroes — only 3
Hero	Role	Simple ability
🛡️ Knight	Tank	High HP
🏹 Archer	Ranged	Attacks from distance
🧙 Mage	AoE	Damages multiple monsters

That's it.

The first battle should look like this
        HUMAN ENTRANCE
              ↓
       🛡️ Knight
       🏹 Archer
       🧙 Mage
              ↓
    ┌───────────────────┐
    │    SPIKE TRAP      │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │    🟢 SLIME       │
    │    🟢 SLIME       │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │   👺 👺 GOBLIN    │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │  ☠️ SKELETON      │
    │  ☠️ SKELETON      │
    └─────────┬─────────┘
              ↓
         💎 TREASURE
              ↓
        💜 DUNGEON CORE

The heroes automatically walk through the dungeon.

Monsters automatically fight.

The player mostly watches their dungeon work.

Keep the player decisions simple too

Before an invasion, the player gets only a few meaningful decisions:

1. Where do I put monsters?
Slime → front
Goblin → behind Slime
Skeleton → final room
2. Where do I put traps?
Spike → entrance
Pit → before Goblins
3. Start invasion

Then:

WATCH.

That's important.

The first prototype shouldn't have 20 buttons during combat.

Give the player one emergency ability

I'd add just one active Dungeon Master ability:

🔮 Dark Magic

Click an enemy → deal a burst of damage.

This gives the player something to do during combat without turning it into an RTS.

Later we can add:

summon monster
heal monster
freeze hero
close door
activate trap

But not yet.

The MVP progression

Keep it almost arcade-like:

        BUILD DUNGEON
              ↓
       RECRUIT MONSTERS
              ↓
       PLACE MONSTERS
              ↓
       START INVASION
              ↓
        AUTO COMBAT
              ↓
      DID THEY SURVIVE?
          ↙        ↘
        YES         NO
         ↓           ↓
      LOOT        DUNGEON
         ↓        DAMAGED
         ↓           ↓
      UPGRADE ←──────┘
         ↓
    NEXT INVASION
First 5 waves

Wave 1

Knight

Wave 2

Knight + Archer

Wave 3

Knight + Archer + Mage

Wave 4

2 Knights + Archer

Wave 5

Full party

That's enough to test whether the layout + auto-combat loop is actually fun.

And I'd keep the art scope equally small

For the first playable version:

Monsters

Slime idle
Slime attack
Goblin idle
Goblin attack
Skeleton idle
Skeleton attack

Heroes

Knight idle/attack/death
Archer idle/attack/death
Mage idle/attack/death

Environment

Floor
Wall
Door
Torch
Spike trap
Slime pool
Treasure
Dungeon Core

That is a very manageable first art set.