"""Rendering system: all draw calls, camera, and scaling."""

from typing import Optional

import pygame

from constants import (
    COLORS,
    GRID_HEIGHT,
    GRID_WIDTH,
    PLAY_AREA_WIDTH,
    SCALE_FACTOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDEBAR_WIDTH,
    TILE_SIZE,
    GameState,
    TileType,
)
from grid import Grid


class Renderer:
    """Handles all rendering to the screen."""

    def __init__(self, display_surface: pygame.Surface, scale: int = SCALE_FACTOR) -> None:
        self._display = display_surface
        self._scale = scale
        self._logical = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._font_large = pygame.font.SysFont("monospace", 24)
        self._font_medium = pygame.font.SysFont("monospace", 16)
        self._font_small = pygame.font.SysFont("monospace", 12)

    def clear(self) -> None:
        """Clear the logical frame."""
        self._logical.fill(COLORS["void_black"])

    def present(self) -> None:
        """Scale logical frame to display and flip buffers."""
        scaled = pygame.transform.scale(self._logical, self._display.get_size())
        self._display.blit(scaled, (0, 0))
        pygame.display.flip()

    def draw_menu(self) -> None:
        """Draw the title screen."""
        self._logical.fill(COLORS["void_black"])

        title = self._font_large.render("DUNGEON KEEP", True, COLORS["heart_purple"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self._logical.blit(title, title_rect)

        subtitle = self._font_medium.render("Click to Start Prototype", True, COLORS["gold_yellow"])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self._logical.blit(subtitle, subtitle_rect)

        hint = self._font_small.render("Build rooms  Recruit monsters  Defend the heart", True, COLORS["ui_border"])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self._logical.blit(hint, hint_rect)

    def draw_game(self, grid: Grid, hover_tile: Optional[tuple] = None) -> None:
        """Draw the play area and sidebar."""
        self._draw_grid(grid, hover_tile)
        self._draw_sidebar()

    def _draw_grid(self, grid: Grid, hover_tile: Optional[tuple] = None) -> None:
        """Render the tile grid in the play area."""
        for y in range(grid.height):
            for x in range(grid.width):
                tile = grid.get_tile(x, y)
                color = self._tile_color(tile)
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self._logical, color, rect)
                pygame.draw.rect(self._logical, COLORS["void_black"], rect, 1)

                # Draw a small indicator for special tiles
                if tile == TileType.DUNGEON_HEART:
                    inner = rect.inflate(-8, -8)
                    pygame.draw.rect(self._logical, COLORS["gold_yellow"], inner, 2)

        # Highlight hovered tile
        if hover_tile:
            hx, hy = hover_tile
            if grid.in_bounds(hx, hy):
                h_rect = pygame.Rect(hx * TILE_SIZE, hy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self._logical, COLORS["gold_yellow"], h_rect, 2)

    def _tile_color(self, tile: TileType) -> tuple:
        """Return the render color for a tile type."""
        mapping = {
            TileType.STONE_FLOOR: COLORS["stone_gray"],
            TileType.STONE_WALL: COLORS["wall_gray"],
            TileType.DUNGEON_HEART: COLORS["heart_purple"],
            TileType.LAIR: COLORS["moss_green"],
            TileType.TRAP_ROOM: COLORS["trap_orange"],
            TileType.TREASURY: COLORS["gold_yellow"],
        }
        return mapping.get(tile, COLORS["stone_gray"])

    def _draw_sidebar(self) -> None:
        """Render the UI sidebar."""
        panel_x = PLAY_AREA_WIDTH
        panel_rect = pygame.Rect(panel_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self._logical, COLORS["wall_gray"], panel_rect)
        pygame.draw.rect(self._logical, COLORS["ui_border"], panel_rect, 2)

        # Header
        header = self._font_medium.render("DUNGEON KEEP", True, COLORS["gold_yellow"])
        self._logical.blit(header, (panel_x + 10, 10))

        # Divider
        pygame.draw.line(
            self._logical,
            COLORS["ui_border"],
            (panel_x + 10, 40),
            (panel_x + SIDEBAR_WIDTH - 10, 40),
            1,
        )

        # Instructions
        lines = [
            "Controls:",
            "Click grid: select",
            "Space: pause",
            "ESC: cancel",
            "",
            "M1 Skeleton",
            "Grid: 16x12",
        ]
        y_offset = 55
        for line in lines:
            text = self._font_small.render(line, True, COLORS["ui_border"])
            self._logical.blit(text, (panel_x + 10, y_offset))
            y_offset += 16

    def draw_pause_overlay(self) -> None:
        """Draw a semi-transparent overlay with PAUSED text."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self._logical.blit(overlay, (0, 0))

        text = self._font_large.render("PAUSED", True, COLORS["gold_yellow"])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self._logical.blit(text, rect)
