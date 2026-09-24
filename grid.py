"""Tile map and pathfinding."""

from typing import List, Optional, Tuple

from constants import GRID_HEIGHT, GRID_WIDTH, TileType


class Grid:
    """16x12 tile grid with boundary walls and Dungeon Heart."""

    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT) -> None:
        self.width = width
        self.height = height
        self._tiles: List[List[TileType]] = [
            [TileType.STONE_FLOOR for _ in range(width)] for _ in range(height)
        ]
        self._setup_boundary_walls()
        self._place_dungeon_heart()

    def _setup_boundary_walls(self) -> None:
        """Place walls around the outer edge."""
        for x in range(self.width):
            self._tiles[0][x] = TileType.STONE_WALL
            self._tiles[self.height - 1][x] = TileType.STONE_WALL
        for y in range(self.height):
            self._tiles[y][0] = TileType.STONE_WALL
            self._tiles[y][self.width - 1] = TileType.STONE_WALL

    def _place_dungeon_heart(self) -> None:
        """Place the Dungeon Heart at the center."""
        cx = self.width // 2
        cy = self.height // 2
        self._tiles[cy][cx] = TileType.DUNGEON_HEART

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within the grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if heroes/monsters can walk on this tile."""
        if not self.in_bounds(x, y):
            return False
        tile = self._tiles[y][x]
        return tile in {TileType.STONE_FLOOR}

    def is_buildable(self, x: int, y: int) -> bool:
        """Return True if a room can be built here."""
        if not self.in_bounds(x, y):
            return False
        return self._tiles[y][x] == TileType.STONE_FLOOR

    def get_tile(self, x: int, y: int) -> TileType:
        """Get the tile type at grid coordinates."""
        if not self.in_bounds(x, y):
            return TileType.STONE_WALL
        return self._tiles[y][x]

    def set_tile(self, x: int, y: int, tile_type: TileType) -> None:
        """Set the tile type at grid coordinates."""
        if self.in_bounds(x, y):
            self._tiles[y][x] = tile_type

    def find_dungeon_heart(self) -> Tuple[int, int]:
        """Find the Dungeon Heart coordinates."""
        for y in range(self.height):
            for x in range(self.width):
                if self._tiles[y][x] == TileType.DUNGEON_HEART:
                    return (x, y)
        return (self.width // 2, self.height // 2)

    def get_path(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """A* pathfinding from start to end. Returns list of grid coordinates."""
        # Placeholder for M1 — straight line fallback
        # Full A* will be implemented in M3
        if start == end:
            return [start]
        return [start, end]
