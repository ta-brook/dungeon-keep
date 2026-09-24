"""Game entities: monsters, heroes, and projectiles."""

from typing import List, Optional, Tuple

from constants import HERO_STATS, MONSTER_STATS, TILE_SIZE
from grid import Grid


class Entity:
    """Base class for all game entities."""

    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        hp: int,
        damage: int,
        attack_speed: float,
        move_speed: float,
        color: Tuple[int, int, int],
    ) -> None:
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = float(grid_x * TILE_SIZE + TILE_SIZE // 2)
        self.y = float(grid_y * TILE_SIZE + TILE_SIZE // 2)
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.attack_speed = attack_speed
        self.move_speed = move_speed  # tiles per second
        self.color = color
        self.attack_cooldown = 0.0
        self.alive = True

    @property
    def position(self) -> Tuple[float, float]:
        """Pixel coordinates."""
        return (self.x, self.y)

    def take_damage(self, amount: int) -> None:
        """Apply damage."""
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def distance_to(self, other: "Entity") -> float:
        """Distance in tiles to another entity."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5 / TILE_SIZE

    def update(self, dt: float, grid: Grid, all_entities: List["Entity"]) -> None:
        """Update entity logic."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt


class Monster(Entity):
    """Player-controlled dungeon monster."""

    def __init__(self, grid_x: int, grid_y: int, monster_type: str) -> None:
        stats = MONSTER_STATS[monster_type]
        color_map = {
            "goblin": MONSTER_STATS["goblin"],
            "slime": (107, 191, 71),
            "skeleton": (212, 212, 212),
        }
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            hp=stats["hp"],
            damage=stats["damage"],
            attack_speed=stats["attack_speed"],
            move_speed=stats["move_speed"],
            color=color_map.get(monster_type, (128, 128, 128)),
        )
        self.monster_type = monster_type
        self.aggro_range = stats["aggro_range"]
        self.target: Optional[Hero] = None

    def update(self, dt: float, grid: Grid, all_entities: List[Entity]) -> None:
        """Update monster AI."""
        super().update(dt, grid, all_entities)
        if not self.alive:
            return

        # Find target
        heroes = [e for e in all_entities if isinstance(e, Hero) and e.alive]
        self.target = self._find_target(heroes)

        if self.target:
            dist = self.distance_to(self.target)
            if dist > 1.0:  # Move toward target
                self._move_toward(self.target, dt, grid)
            # Attack handled in combat.py

    def _find_target(self, heroes: List["Hero"]) -> Optional["Hero"]:
        """Find nearest hero within aggro range."""
        nearest = None
        nearest_dist = float("inf")
        for hero in heroes:
            dist = self.distance_to(hero)
            if dist <= self.aggro_range and dist < nearest_dist:
                nearest = hero
                nearest_dist = dist
        return nearest

    def _move_toward(self, target: Entity, dt: float, grid: Grid) -> None:
        """Move toward target entity."""
        dx = target.x - self.x
        dy = target.y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.1:
            return

        speed = self.move_speed * TILE_SIZE * dt
        self.x += (dx / dist) * speed
        self.y += (dy / dist) * speed

        # Snap to grid for walkability checks
        gx = int(self.x // TILE_SIZE)
        gy = int(self.y // TILE_SIZE)
        if grid.is_walkable(gx, gy):
            self.grid_x = gx
            self.grid_y = gy
        else:
            # Revert if invalid
            self.x -= (dx / dist) * speed
            self.y -= (dy / dist) * speed


class Hero(Entity):
    """Invading hero unit."""

    def __init__(self, grid_x: int, grid_y: int, hero_type: str) -> None:
        stats = HERO_STATS[hero_type]
        color_map = {
            "adventurer": (201, 76, 76),
            "knight": (138, 155, 184),
            "paladin": (212, 175, 55),
        }
        super().__init__(
            grid_x=grid_x,
            grid_y=grid_y,
            hp=stats["hp"],
            damage=stats["damage"],
            attack_speed=stats["attack_speed"],
            move_speed=stats["move_speed"],
            color=color_map.get(hero_type, (255, 0, 0)),
        )
        self.hero_type = hero_type
        self.path: List[Tuple[int, int]] = []
        self.path_timer = 0.0
        self.path_target: Optional[Tuple[int, int]] = None

    def set_path(self, path: List[Tuple[int, int]]) -> None:
        """Set movement path."""
        self.path = path
        self.path_target = None

    def update(self, dt: float, grid: Grid, all_entities: List[Entity]) -> None:
        """Update hero AI."""
        super().update(dt, grid, all_entities)
        if not self.alive:
            return

        # Recalculate path periodically
        self.path_timer += dt
        if self.path_timer >= 0.5 or not self.path:
            self.path_timer = 0.0
            heart = grid.find_dungeon_heart()
            self.path = grid.get_path((self.grid_x, self.grid_y), heart)

        # Follow path
        if len(self.path) > 1:
            next_tile = self.path[1]
            self._move_to_tile(next_tile, dt, grid)
            # Check if reached next tile
            if self.grid_x == next_tile[0] and self.grid_y == next_tile[1]:
                self.path.pop(0)

    def _move_to_tile(
        self, target_tile: Tuple[int, int], dt: float, grid: Grid
    ) -> None:
        """Move toward a specific grid tile."""
        target_x = target_tile[0] * TILE_SIZE + TILE_SIZE // 2
        target_y = target_tile[1] * TILE_SIZE + TILE_SIZE // 2

        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.1:
            self.grid_x = target_tile[0]
            self.grid_y = target_tile[1]
            return

        speed = self.move_speed * TILE_SIZE * dt
        move_dist = min(speed, dist)
        self.x += (dx / dist) * move_dist
        self.y += (dy / dist) * move_dist

        # Update grid position
        gx = int(self.x // TILE_SIZE)
        gy = int(self.y // TILE_SIZE)
        if grid.in_bounds(gx, gy):
            self.grid_x = gx
            self.grid_y = gy
