"""Game constants, enums, and configuration."""

from enum import Enum, auto

# Screen dimensions (logical)
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 384

# Play area and sidebar
PLAY_AREA_WIDTH = 512
SIDEBAR_WIDTH = 256

# Grid dimensions (large tiles, fewer rooms — Dungeon Maker style)
GRID_WIDTH = 6
GRID_HEIGHT = 4
TILE_SIZE = 72

# Grid offset to center it in the play area
GRID_OFFSET_X = (PLAY_AREA_WIDTH - GRID_WIDTH * TILE_SIZE) // 2  # (512 - 432) // 2 = 40
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT * TILE_SIZE) // 2   # (384 - 288) // 2 = 48

# Rendering
SCALE_FACTOR = 2
FPS = 60

# Economy
STARTING_GOLD = 150

# Room costs
ROOM_COSTS = {
    "LAIR": 50,
    "TRAP_ROOM": 40,
    "TREASURY": 60,
}

# Monster costs
MONSTER_COSTS = {
    "goblin": 20,
    "slime": 15,
    "skeleton": 30,
}

# Income
TREASURY_GOLD_PER_SECOND = 1
HERO_KILL_GOLD = 10

# Monster stats (HP, Damage, Attack Speed, Move Speed in tiles/s, Aggro Range in tiles)
MONSTER_STATS = {
    "goblin": {"hp": 30, "damage": 5, "attack_speed": 1.0, "move_speed": 2.0, "aggro_range": 3.0},
    "slime": {"hp": 50, "damage": 3, "attack_speed": 0.8, "move_speed": 1.0, "aggro_range": 3.0},
    "skeleton": {"hp": 40, "damage": 8, "attack_speed": 0.6, "move_speed": 1.5, "aggro_range": 3.0},
}

# Hero stats (HP, Damage, Attack Speed, Move Speed in tiles/s)
HERO_STATS = {
    "adventurer": {"hp": 40, "damage": 5, "attack_speed": 1.0, "move_speed": 0.5},
    "knight": {"hp": 80, "damage": 8, "attack_speed": 0.8, "move_speed": 0.4},
    "paladin": {"hp": 150, "damage": 12, "attack_speed": 0.6, "move_speed": 0.3},
}

# Wave definitions: list of (hero_type, count)
WAVES = [
    [("adventurer", 3)],
    [("adventurer", 4), ("knight", 2)],
    [("adventurer", 5), ("knight", 3), ("paladin", 1)],
]

# Spawn interval between heroes in a wave
SPAWN_INTERVAL = 2.0

# Time between waves
WAVE_COOLDOWN = 5.0

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
    "entrance_brown": (107, 68, 35),
}


class TileType(Enum):
    """Types of tiles on the grid."""

    STONE_FLOOR = auto()
    STONE_WALL = auto()
    DUNGEON_HEART = auto()
    ENTRANCE = auto()
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
