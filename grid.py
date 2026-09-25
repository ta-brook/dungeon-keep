"""Tile map and pathfinding."""

import heapq
import random
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
        self._floor_variants: List[List[int]] = [
            [random.randint(0, 15) for _ in range(width)] for _ in range(height)
        ]
        self._place_entrance()
        self._place_dungeon_heart()
        self._setup_boundary_walls()

    def _setup_boundary_walls(self) -> None:
        """Place walls around the outer edge, but leave room for Entrance and Heart."""
        for x in range(self.width):
            self._tiles[0][x] = TileType.STONE_WALL
            self._tiles[self.height - 1][x] = TileType.STONE_WALL
        for y in range(self.height):
            # Don't overwrite Entrance (left edge) or Heart (right edge)
            if self._tiles[y][0] != TileType.ENTRANCE:
                self._tiles[y][0] = TileType.STONE_WALL
            if self._tiles[y][self.width - 1] != TileType.DUNGEON_HEART:
                self._tiles[y][self.width - 1] = TileType.STONE_WALL

    def _place_entrance(self) -> None:
        """Place the Entrance on the left edge."""
        ey = self.height // 2
        self._tiles[ey][0] = TileType.ENTRANCE

    def _place_dungeon_heart(self) -> None:
        """Place the Dungeon Heart on the right edge."""
        cx = self.width - 1
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
        return tile in {TileType.STONE_FLOOR, TileType.DUNGEON_HEART, TileType.ENTRANCE}

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

    def get_floor_variant(self, x: int, y: int) -> int:
        """Get the floor tile variation index at grid coordinates."""
        if not self.in_bounds(x, y):
            return 0
        return self._floor_variants[y][x]

    def find_dungeon_heart(self) -> Tuple[int, int]:
        """Find the Dungeon Heart coordinates."""
        for y in range(self.height):
            for x in range(self.width):
                if self._tiles[y][x] == TileType.DUNGEON_HEART:
                    return (x, y)
        return (self.width // 2, self.height // 2)

    def find_entrance(self) -> Tuple[int, int]:
        """Find the Entrance coordinates."""
        for y in range(self.height):
            for x in range(self.width):
                if self._tiles[y][x] == TileType.ENTRANCE:
                    return (x, y)
        return (1, self.height // 2)

    def get_path(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """A* pathfinding from start to end. Returns list of grid coordinates."""
        if start == end:
            return [start]

        # A* implementation
        open_set = [(0, start)]
        came_from: dict = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, end)}
        open_set_hash = {start}

        while open_set:
            _, current = heapq.heappop(open_set)
            open_set_hash.discard(current)

            if current == end:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

        # No path found — return straight line fallback
        return [start, end]

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get walkable neighboring tiles."""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def _reconstruct_path(
        self, came_from: dict, current: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """Reconstruct path from A* search."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
