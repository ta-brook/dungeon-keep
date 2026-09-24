"""Game constants, enums, and configuration."""

from enum import Enum, auto

# Screen dimensions (logical)
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 384

# Play area and sidebar
PLAY_AREA_WIDTH = 512
SIDEBAR_WIDTH = 256

# Grid dimensions
GRID_WIDTH = 16
GRID_HEIGHT = 12
TILE_SIZE = 32

# Rendering
SCALE_FACTOR = 2
FPS = 60

# Colors (RGB tuples) from PALETTE.md
COLORS = {
    "void_black": (13, 13, 13),
    "stone_gray": (74, 74, 74),
    "wall_gray": (43, 43, 43),
    "moss_green": (61, 92, 58),
    "ui_border": (122, 122, 122),
    "slime_green": (107, 191, 71),
    "goblin_skin": (92, 138, 69),
    "bone_white": (212, 212, 212),
    "hero_red": (201, 76, 76),
    "knight_steel": (138, 155, 184),
    "paladin_gold": (212, 175, 55),
    "heart_purple": (138, 43, 226),
    "gold_yellow": (255, 215, 0),
    "trap_orange": (204, 85, 0),
    "blood_red": (139, 0, 0),
}


class TileType(Enum):
    """Types of tiles on the grid."""

    STONE_FLOOR = auto()
    STONE_WALL = auto()
    DUNGEON_HEART = auto()
    LAIR = auto()
    TRAP_ROOM = auto()
    TREASURY = auto()


class GameState(Enum):
    """High-level game states."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    WIN = auto()
    LOSS = auto()
