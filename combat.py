"""Combat resolution, targeting, and cooldowns."""

from typing import List, Optional

from constants import TILE_SIZE
from entities import Entity, Hero, Monster
from grid import Grid


def resolve_combat(attacker: Entity, target: Entity, dt: float) -> bool:
    """Process one combat tick. Returns True if target died."""
    if not attacker.alive or not target.alive:
        return False

    dist = attacker.distance_to(target)
    if dist > 1.2:  # Attack range in tiles
        return False

    if attacker.attack_cooldown > 0:
        return False

    # Deal damage
    target.take_damage(attacker.damage)
    attacker.attack_cooldown = 1.0 / attacker.attack_speed

    return not target.alive


def find_nearest_enemy(
    entity: Entity, enemies: List[Entity], max_range: float
) -> Optional[Entity]:
    """Find the nearest enemy within range."""
    nearest = None
    nearest_dist = float("inf")
    for enemy in enemies:
        if not enemy.alive:
            continue
        dist = entity.distance_to(enemy)
        if dist <= max_range and dist < nearest_dist:
            nearest = enemy
            nearest_dist = dist
    return nearest


def apply_trap_damage(heroes: List[Hero], grid: Grid, dt: float) -> int:
    """Apply damage to heroes adjacent to trap rooms. Returns gold earned."""
    gold_earned = 0
    trap_damage_per_sec = 5
    damage = trap_damage_per_sec * dt

    # Find all trap rooms
    traps = []
    for y in range(grid.height):
        for x in range(grid.width):
            from constants import TileType
            if grid.get_tile(x, y) == TileType.TRAP_ROOM:
                traps.append((x, y))

    # Damage heroes on adjacent tiles
    for hero in heroes:
        if not hero.alive:
            continue
        for tx, ty in traps:
            if abs(hero.grid_x - tx) <= 1 and abs(hero.grid_y - ty) <= 1:
                if hero.grid_x != tx or hero.grid_y != ty:
                    hero.take_damage(int(damage))
                    if not hero.alive:
                        from constants import HERO_KILL_GOLD
                        gold_earned += HERO_KILL_GOLD
                    break

    return gold_earned


def update_all_combat(
    monsters: List[Monster],
    heroes: List[Hero],
    grid: Grid,
    dt: float,
) -> int:
    """Update all combat for one frame. Returns gold earned from hero deaths."""
    gold_earned = 0

    # Monsters attack heroes
    for monster in monsters:
        if not monster.alive:
            continue
        target = find_nearest_enemy(monster, heroes, 1.2)
        if target:
            if resolve_combat(monster, target, dt):
                gold_earned += 10

    # Heroes attack monsters or Dungeon Heart
    for hero in heroes:
        if not hero.alive:
            continue

        # Try to attack monster first
        target = find_nearest_enemy(hero, monsters, 1.2)
        if target:
            resolve_combat(hero, target, dt)
        else:
            # Check if at Dungeon Heart
            heart = grid.find_dungeon_heart()
            if hero.grid_x == heart[0] and hero.grid_y == heart[1]:
                # Hero reached the heart — for now just mark as damaging
                pass

    # Apply trap damage
    gold_earned += apply_trap_damage(heroes, grid, dt)

    return gold_earned
