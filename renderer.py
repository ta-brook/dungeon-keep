"""Rendering system: all draw calls, camera, and scaling."""

from typing import List, Optional

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
from entities import Entity, Hero, Monster
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
        monsters: List[Monster],
        heroes: List[Hero],
        hover_tile: Optional[tuple] = None,
        build_valid: Optional[bool] = None,
        wave_info: str = "",
    ) -> None:
        """Draw the play area and sidebar."""
        self._draw_grid(grid, hover_tile, build_valid)
        self._draw_trap_indicators(grid)
        self._draw_entities(monsters, heroes)
        ui.draw(self._logical)

        # Wave info
        if wave_info:
            wave_text = self._font_small.render(wave_info, True, COLORS["blood_red"])
            self._logical.blit(wave_text, (10, SCREEN_HEIGHT - 20))

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
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_tile(x, y) == TileType.TRAP_ROOM:
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

    def _draw_entities(self, monsters: List[Monster], heroes: List[Hero]) -> None:
        """Draw all monsters and heroes with HP bars."""
        # Draw monsters
        for monster in monsters:
            if not monster.alive:
                continue
            self._draw_entity(monster, monster.color)

        # Draw heroes
        for hero in heroes:
            if not hero.alive:
                continue
            self._draw_entity(hero, hero.color)

    def _draw_entity(self, entity: Entity, color: tuple) -> None:
        """Draw a single entity with HP bar."""
        # Body
        rect = pygame.Rect(
            int(entity.x - 8),
            int(entity.y - 8),
            16,
            16,
        )
        pygame.draw.rect(self._logical, color, rect)
        pygame.draw.rect(self._logical, COLORS["void_black"], rect, 1)

        # HP bar background
        hp_bg = pygame.Rect(
            int(entity.x - 10),
            int(entity.y - 14),
            20,
            4,
        )
        pygame.draw.rect(self._logical, COLORS["void_black"], hp_bg)

        # HP bar fill
        if entity.max_hp > 0:
            hp_ratio = entity.hp / entity.max_hp
            hp_width = int(18 * hp_ratio)
            hp_fill = pygame.Rect(
                int(entity.x - 9),
                int(entity.y - 13),
                hp_width,
                2,
            )
            hp_color = COLORS["slime_green"] if hp_ratio > 0.5 else COLORS["trap_orange"] if hp_ratio > 0.25 else COLORS["blood_red"]
            pygame.draw.rect(self._logical, hp_color, hp_fill)

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

    def draw_win_screen(self) -> None:
        """Draw win screen overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self._logical.blit(overlay, (0, 0))

        text = self._font_large.render("VICTORY!", True, COLORS["gold_yellow"])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self._logical.blit(text, rect)

        sub = self._font_medium.render("Dungeon secured", True, COLORS["slime_green"])
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self._logical.blit(sub, sub_rect)

    def draw_loss_screen(self) -> None:
        """Draw loss screen overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self._logical.blit(overlay, (0, 0))

        text = self._font_large.render("DEFEAT", True, COLORS["blood_red"])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self._logical.blit(text, rect)

        sub = self._font_medium.render("Dungeon Heart destroyed", True, COLORS["trap_orange"])
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self._logical.blit(sub, sub_rect)
