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
    TileType,
)
from grid import Grid
from ui import UI


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

    def draw_game(
        self,
        grid: Grid,
        ui: UI,
        hover_tile: Optional[tuple] = None,
        build_valid: Optional[bool] = None,
    ) -> None:
        """Draw the play area and sidebar."""
        self._draw_grid(grid, hover_tile, build_valid)
        self._draw_trap_indicators(grid)
        ui.draw(self._logical)

    def _draw_grid(
        self,
        grid: Grid,
        hover_tile: Optional[tuple] = None,
        build_valid: Optional[bool] = None,
    ) -> None:
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
                if build_valid is True:
                    pygame.draw.rect(self._logical, COLORS["slime_green"], h_rect, 2)
                elif build_valid is False:
                    pygame.draw.rect(self._logical, COLORS["blood_red"], h_rect, 2)
                else:
                    pygame.draw.rect(self._logical, COLORS["gold_yellow"], h_rect, 2)

    def _draw_trap_indicators(self, grid: Grid) -> None:
        """Draw warning indicators on tiles adjacent to trap rooms."""
        trap_color = (*COLORS["trap_orange"][:3], 80)  # semi-transparent
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_tile(x, y) == TileType.TRAP_ROOM:
                    # Draw small indicators on adjacent floor tiles
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ax, ay = x + dx, y + dy
                            if grid.in_bounds(ax, ay) and grid.get_tile(ax, ay) == TileType.STONE_FLOOR:
                                rect = pygame.Rect(
                                    ax * TILE_SIZE + 8,
                                    ay * TILE_SIZE + 8,
                                    16,
                                    16,
                                )
                                pygame.draw.rect(self._logical, COLORS["trap_orange"], rect)

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

    def draw_pause_overlay(self) -> None:
        """Draw a semi-transparent overlay with PAUSED text."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self._logical.blit(overlay, (0, 0))

        text = self._font_large.render("PAUSED", True, COLORS["gold_yellow"])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self._logical.blit(text, rect)
