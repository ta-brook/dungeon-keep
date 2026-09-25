"""Game entities: monsters, heroes, and projectiles."""

import math
from typing import List, Optional, Tuple

from constants import HERO_STATS, MONSTER_STATS, TILE_SIZE
from grid import Grid


def angle_to_direction(angle: float) -> str:
    """Convert an angle (radians) to one of 8 directions."""
    # Normalize angle to 0-2PI
    angle = angle % (2 * math.pi)
    # 8 directions: divide circle into 8 segments
    # Each segment is PI/4 (45 degrees)
    # 0 = east, PI/4 = south-east, PI/2 = south, etc.
    directions = [
        "east",         # 0 to PI/8
        "south-east",   # PI/8 to 3PI/8
        "south",        # 3PI/8 to 5PI/8
        "south-west",   # 5PI/8 to 7PI/8
        "west",         # 7PI/8 to 9PI/8
        "north-west",   # 9PI/8 to 11PI/8
        "north",        # 11PI/8 to 13PI/8
        "north-east",   # 13PI/8 to 15PI/8
        "east",         # 15PI/8 to 2PI
    ]
    segment = int((angle + math.pi / 8) / (math.pi / 4))
    return directions[min(segment, 8)]


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
        """Update monster — stationary defender. Only reduces cooldowns."""
        super().update(dt, grid, all_entities)
        # Monsters are stationary in Battle Rooms; combat is handled in combat.py


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
        self.animation_timer = 0.0
        self.facing_direction = "south"
        self.is_moving = False
        # Discrete step movement: timer counts down between tile jumps
        self.move_timer = 1.0 / self.move_speed

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

        # Follow path — discrete tile steps
        if len(self.path) > 1:
            self.move_timer -= dt
            if self.move_timer <= 0:
                next_tile = self.path[1]
                # Move to next tile (always adjacent in a valid path)
                # If not adjacent, step one tile toward it as a safety fallback
                dx = max(-1, min(1, next_tile[0] - self.grid_x))
                dy = max(-1, min(1, next_tile[1] - self.grid_y))
                self.grid_x += dx
                self.grid_y += dy
                self.x = self.grid_x * TILE_SIZE + TILE_SIZE // 2
                self.y = self.grid_y * TILE_SIZE + TILE_SIZE // 2

                # Remove the tile we just left from the path
                self.path.pop(0)
                # If we landed on what was path[1], it's now path[0] — remove it too
                if self.path and self.grid_x == self.path[0][0] and self.grid_y == self.path[0][1]:
                    self.path.pop(0)

                self.move_timer = 1.0 / self.move_speed

                # Face the next upcoming tile (if any)
                if len(self.path) > 1:
                    dx = self.path[1][0] - self.grid_x
                    dy = self.path[1][1] - self.grid_y
                    angle = math.atan2(dy, dx)
                    self.facing_direction = angle_to_direction(-angle)

                # Brief moving flag for animation
                self.is_moving = True
                self.animation_timer = 0.0
            else:
                self.is_moving = False
        else:
            self.is_moving = False

    def _move_to_tile(
        self, target_tile: Tuple[int, int], dt: float, grid: Grid
    ) -> None:
        """Legacy smooth-move helper; heroes now move discretely in update()."""
        pass
