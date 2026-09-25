"""Input handling: translate Pygame events to game actions."""

from typing import Callable, Optional, Tuple

import pygame

from constants import GRID_HEIGHT, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_WIDTH, PLAY_AREA_WIDTH, SCALE_FACTOR, TILE_SIZE


class InputHandler:
    """Translates raw Pygame events into game commands."""

    def __init__(self) -> None:
        self.on_grid_click: Optional[Callable[[int, int], None]] = None
        self.on_pause_toggle: Optional[Callable[[], None]] = None
        self.on_menu_start: Optional[Callable[[], None]] = None
        self.on_escape: Optional[Callable[[], None]] = None

    def process(self, event: pygame.event.Event) -> None:
        """Process a single Pygame event."""
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_pause_toggle:
                self.on_pause_toggle()
            if event.key == pygame.K_ESCAPE and self.on_escape:
                self.on_escape()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def _handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle a left mouse click."""
        # Scale down from display coordinates to logical coordinates
        logical_x = pos[0] // SCALE_FACTOR
        logical_y = pos[1] // SCALE_FACTOR

        if logical_x < PLAY_AREA_WIDTH:
            # Grid area (accounting for grid offset)
            grid_x = (logical_x - GRID_OFFSET_X) // TILE_SIZE
            grid_y = (logical_y - GRID_OFFSET_Y) // TILE_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if self.on_grid_click:
                    self.on_grid_click(grid_x, grid_y)
        else:
            # Sidebar area — handled in UI module later
            pass

    def get_mouse_logical_pos(self) -> Tuple[int, int]:
        """Return current mouse position in logical coordinates."""
        mx, my = pygame.mouse.get_pos()
        return (mx // SCALE_FACTOR, my // SCALE_FACTOR)
