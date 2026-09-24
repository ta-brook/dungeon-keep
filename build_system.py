"""Room placement validation and economy."""

from typing import List, Optional, Tuple

from constants import (
    HERO_KILL_GOLD,
    MONSTER_COSTS,
    ROOM_COSTS,
    STARTING_GOLD,
    TREASURY_GOLD_PER_SECOND,
    TileType,
)
from entities import Monster
from grid import Grid


class BuildSystem:
    """Handles building rooms, recruiting monsters, and gold economy."""

    def __init__(self, grid: Grid, starting_gold: int = STARTING_GOLD) -> None:
        self._grid = grid
        self._gold = starting_gold
        self._income_timer = 0.0

    @property
    def gold(self) -> int:
        """Current gold amount."""
        return self._gold

    def add_gold(self, amount: int) -> None:
        """Add gold to the treasury."""
        self._gold += amount

    def can_build(self, x: int, y: int, room_type: TileType) -> bool:
        """Check if a room can be built at the given location."""
        if not self._grid.is_buildable(x, y):
            return False

        cost = self._get_room_cost(room_type)
        if cost is None:
            return False

        return self._gold >= cost

    def build(self, x: int, y: int, room_type: TileType) -> bool:
        """Build a room and deduct gold. Returns True on success."""
        if not self.can_build(x, y, room_type):
            return False

        cost = self._get_room_cost(room_type)
        if cost is None:
            return False

        self._gold -= cost
        self._grid.set_tile(x, y, room_type)
        return True

    def can_recruit(self, monster_type: str) -> bool:
        """Check if a monster can be recruited."""
        cost = MONSTER_COSTS.get(monster_type)
        if cost is None:
            return False
        return self._gold >= cost

    def recruit(self, lair_x: int, lair_y: int, monster_type: str) -> Optional[Monster]:
        """Recruit a monster at a Lair. Returns the monster or None."""
        if self._grid.get_tile(lair_x, lair_y) != TileType.LAIR:
            return None

        cost = MONSTER_COSTS.get(monster_type)
        if cost is None:
            return None

        if self._gold < cost:
            return None

        self._gold -= cost
        return Monster(lair_x, lair_y, monster_type)

    def update(self, dt: float) -> int:
        """Update economy tick. Returns gold earned this frame."""
        earned = 0

        # Treasury passive income
        self._income_timer += dt
        if self._income_timer >= 1.0:
            self._income_timer -= 1.0
            treasury_count = self._count_treasuries()
            income = treasury_count * TREASURY_GOLD_PER_SECOND
            self._gold += income
            earned += income

        return earned

    def _get_room_cost(self, room_type: TileType) -> Optional[int]:
        """Get the gold cost for a room type."""
        mapping = {
            TileType.LAIR: ROOM_COSTS["LAIR"],
            TileType.TRAP_ROOM: ROOM_COSTS["TRAP_ROOM"],
            TileType.TREASURY: ROOM_COSTS["TREASURY"],
        }
        return mapping.get(room_type)

    def _count_treasuries(self) -> int:
        """Count how many Treasury rooms exist."""
        count = 0
        for y in range(self._grid.height):
            for x in range(self._grid.width):
                if self._grid.get_tile(x, y) == TileType.TREASURY:
                    count += 1
        return count

    @staticmethod
    def get_room_name(room_type: TileType) -> str:
        """Get display name for a room type."""
        names = {
            TileType.LAIR: "Lair",
            TileType.TRAP_ROOM: "Trap",
            TileType.TREASURY: "Treasury",
        }
        return names.get(room_type, "Unknown")

    @staticmethod
    def get_monster_name(monster_type: str) -> str:
        """Get display name for a monster type."""
        names = {
            "goblin": "Goblin",
            "slime": "Slime",
            "skeleton": "Skeleton",
        }
        return names.get(monster_type, "Unknown")
