"""Rendering system: all draw calls, camera, and scaling."""

import math
from typing import List, Optional

import pygame

from assets import AssetRegistry
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

    def __init__(
        self,
        display_surface: pygame.Surface,
        assets: AssetRegistry,
        scale: int = SCALE_FACTOR,
    ) -> None:
        self._display = display_surface
        self._assets = assets
        self._scale = scale
        self._logical = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._font_large = pygame.font.SysFont("monospace", 24)
        self._font_medium = pygame.font.SysFont("monospace", 16)
        self._font_small = pygame.font.SysFont("monospace", 12)
        self._time = 0.0
        self.cursor_mode = "select"  # select, build, recruit
        self._walk_frames: dict = {}  # Cache for walk animation frames

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
        dt: float = 0.0,
        mouse_pos: tuple = (0, 0),
        heart_hp: int = 100,
        heart_max_hp: int = 100,
    ) -> None:
        """Draw the play area and sidebar."""
        self._time += dt
        self._draw_grid(grid, hover_tile, build_valid)
        self._draw_trap_indicators(grid)
        self._draw_entities(monsters, heroes)
        self._draw_dungeon_master(grid)
        ui.draw(self._logical)
        self._draw_custom_cursor(mouse_pos)

        # Wave info
        if wave_info:
            wave_text = self._font_small.render(wave_info, True, COLORS["blood_red"])
            self._logical.blit(wave_text, (10, SCREEN_HEIGHT - 20))

        # Dungeon Heart HP bar
        self._draw_heart_hp(heart_hp, heart_max_hp)

    def _draw_grid(
        self,
        grid: Grid,
        hover_tile: Optional[tuple] = None,
        build_valid: Optional[bool] = None,
    ) -> None:
        """Render the tile grid in the play area."""
        has_floor_assets = self._assets.has_floor_variants()

        for y in range(grid.height):
            for x in range(grid.width):
                tile = grid.get_tile(x, y)
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                if tile == TileType.STONE_FLOOR and has_floor_assets:
                    # Draw floor variant
                    floor_surf = self._assets.get_random_floor()
                    if floor_surf:
                        self._logical.blit(floor_surf, rect)
                    else:
                        pygame.draw.rect(self._logical, COLORS["stone_gray"], rect)
                else:
                    # Draw colored tile or sprite
                    sprite = self._get_tile_sprite(tile)
                    if sprite:
                        self._logical.blit(sprite, rect)
                    else:
                        color = self._tile_color(tile)
                        pygame.draw.rect(self._logical, color, rect)

                # Grid border
                pygame.draw.rect(self._logical, COLORS["void_black"], rect, 1)

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

    def _get_tile_sprite(self, tile: TileType) -> Optional[pygame.Surface]:
        """Get sprite for a tile type if available."""
        mapping = {
            TileType.STONE_WALL: "tile_stone_wall",
            TileType.DUNGEON_HEART: "tile_dungeon_heart",
            TileType.ENTRANCE: "tile_entrance",
            TileType.LAIR: "tile_lair",
            TileType.TRAP_ROOM: "tile_trap_room",
            TileType.TREASURY: "tile_treasury",
        }
        sprite_id = mapping.get(tile)
        if sprite_id:
            return self._assets.get(sprite_id)
        return None

    def _draw_trap_indicators(self, grid: Grid) -> None:
        """Draw warning indicators on trap room tiles."""
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_tile(x, y) == TileType.TRAP_ROOM:
                    # Draw a small warning symbol on the trap tile itself
                    rect = pygame.Rect(
                        x * TILE_SIZE + 10,
                        y * TILE_SIZE + 10,
                        12,
                        12,
                    )
                    pygame.draw.rect(self._logical, COLORS["trap_orange"], rect)

    def _draw_entities(self, monsters: List[Monster], heroes: List[Hero]) -> None:
        """Draw all monsters and heroes with HP bars."""
        # Draw monsters
        for monster in monsters:
            if not monster.alive:
                continue
            self._draw_entity(monster)

        # Draw heroes
        for hero in heroes:
            if not hero.alive:
                continue
            self._draw_entity(hero)

    def _get_entity_sprite(self, entity: Entity) -> Optional[pygame.Surface]:
        """Get sprite for an entity if available."""
        if isinstance(entity, Monster):
            mapping = {
                "goblin": "unit_goblin_idle",
                "slime": "unit_slime_idle",
                "skeleton": "unit_skeleton_idle",
            }
            sprite_id = mapping.get(entity.monster_type)
            if sprite_id:
                return self._assets.get(sprite_id)
        elif isinstance(entity, Hero):
            # Use animated knight sprites for knight/paladin
            if entity.hero_type in ("knight", "adventurer", "paladin"):
                return self._get_hero_sprite(entity)
        return None

    def _get_hero_sprite(self, hero: Hero) -> Optional[pygame.Surface]:
        """Get the appropriate sprite for a hero, with animation."""
        if hero.is_moving:
            # Cycle through walk animation frames
            frame_duration = 0.1  # seconds per frame
            frame_index = int(hero.animation_timer / frame_duration) % 8
            frame_path = f"assets/units/knight_anims/walk/frame_{frame_index:02d}.png"
            if frame_path in self._walk_frames:
                return self._walk_frames[frame_path]
            # Load and cache frame
            try:
                surf = pygame.image.load(frame_path).convert_alpha()
                self._walk_frames[frame_path] = surf
                return surf
            except Exception:
                pass
        
        # Idle or fallback
        return self._assets.get("hero_knight")

    def _draw_entity(self, entity: Entity) -> None:
        """Draw a single entity with sprite or colored rectangle fallback."""
        sprite = self._get_entity_sprite(entity)
        
        if sprite:
            # Center sprite on entity position
            x = int(entity.x - sprite.get_width() // 2)
            y = int(entity.y - sprite.get_height() // 2)
            self._logical.blit(sprite, (x, y))
        else:
            # Fallback: colored rectangle
            rect = pygame.Rect(
                int(entity.x - 8),
                int(entity.y - 8),
                16,
                16,
            )
            pygame.draw.rect(self._logical, entity.color, rect)
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

    def _draw_dungeon_master(self, grid: Grid) -> None:
        """Draw the dungeon master NPC near the Dungeon Heart with bob animation."""
        dm_surf = self._assets.get_dungeon_master()
        if not dm_surf:
            return

        heart = grid.find_dungeon_heart()
        # Place DM one tile below the heart
        dm_x = heart[0] * TILE_SIZE
        dm_y = heart[1] * TILE_SIZE + TILE_SIZE

        # Bob animation: offset y by 0-2 pixels using sine wave
        bob_offset = int(math.sin(self._time * 3) * 2)

        self._logical.blit(dm_surf, (dm_x, dm_y + bob_offset))

    def _draw_custom_cursor(self, mouse_pos: tuple) -> None:
        """Draw custom cursor sprite at mouse position."""
        cursor_map = {
            "build": "cursor_build",
            "recruit": "cursor_recruit",
            "select": "cursor_select",
        }
        sprite_id = cursor_map.get(self.cursor_mode, "cursor_select")
        cursor_surf = self._assets.get(sprite_id)

        if cursor_surf:
            self._logical.blit(cursor_surf, mouse_pos)
        else:
            # Fallback: simple crosshair
            x, y = mouse_pos
            pygame.draw.line(self._logical, COLORS["gold_yellow"], (x - 4, y), (x + 4, y), 1)
            pygame.draw.line(self._logical, COLORS["gold_yellow"], (x, y - 4), (x, y + 4), 1)

    def _draw_heart_hp(self, heart_hp: int, heart_max_hp: int) -> None:
        """Draw Dungeon Heart HP bar above the heart tile."""
        heart = self._logical  # using logical surface
        # Find heart position (we know it's at center from grid)
        from constants import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE
        hx = GRID_WIDTH // 2 * TILE_SIZE
        hy = GRID_HEIGHT // 2 * TILE_SIZE - 8
        bar_w = 32
        bar_h = 4
        ratio = max(0, heart_hp / heart_max_hp)
        fill_w = int(bar_w * ratio)
        bg_rect = pygame.Rect(hx, hy, bar_w, bar_h)
        fill_rect = pygame.Rect(hx, hy, fill_w, bar_h)
        pygame.draw.rect(self._logical, COLORS["void_black"], bg_rect)
        color = COLORS["slime_green"] if ratio > 0.5 else COLORS["trap_orange"] if ratio > 0.25 else COLORS["blood_red"]
        pygame.draw.rect(self._logical, color, fill_rect)

    def _tile_color(self, tile: TileType) -> tuple:
        """Return the render color for a tile type."""
        mapping = {
            TileType.STONE_FLOOR: COLORS["stone_gray"],
            TileType.STONE_WALL: COLORS["wall_gray"],
            TileType.DUNGEON_HEART: COLORS["heart_purple"],
            TileType.ENTRANCE: COLORS["entrance_brown"],
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

        restart = self._font_small.render("Press ENTER to Restart", True, COLORS["gold_yellow"])
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self._logical.blit(restart, restart_rect)

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

        restart = self._font_small.render("Press ENTER to Restart", True, COLORS["gold_yellow"])
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self._logical.blit(restart, restart_rect)
