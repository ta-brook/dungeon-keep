"""Entry point and main game loop."""

import sys

import pygame

from assets import AssetRegistry
from constants import FPS, SCALE_FACTOR, SCREEN_HEIGHT, SCREEN_WIDTH, GameState
from game_state import StateMachine
from grid import Grid
from input_handler import InputHandler
from renderer import Renderer


def main() -> None:
    """Initialize and run the game."""
    pygame.init()

    # Create display window (scaled up for crisp pixel art)
    display_width = SCREEN_WIDTH * SCALE_FACTOR
    display_height = SCREEN_HEIGHT * SCALE_FACTOR
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Dungeon Keep — Prototype")

    clock = pygame.time.Clock()

    # Load assets (generates placeholders on first run)
    assets = AssetRegistry()
    assets.load_all()

    # Game systems
    state_machine = StateMachine(initial_state=GameState.MENU)
    grid = Grid()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    # Track hovered tile for highlighting
    hovered_tile: tuple | None = None

    # Wire up input callbacks
    def on_grid_click(x: int, y: int) -> None:
        tile = grid.get_tile(x, y)
        print(f"Clicked tile ({x}, {y}): {tile.name}")

    def on_pause_toggle() -> None:
        if state_machine.state == GameState.PLAYING:
            state_machine.change_state(GameState.PAUSED)
            print("Game paused")
        elif state_machine.state == GameState.PAUSED:
            state_machine.change_state(GameState.PLAYING)
            print("Game resumed")

    def on_menu_start() -> None:
        if state_machine.state == GameState.MENU:
            state_machine.change_state(GameState.PLAYING)
            print("Game started")

    def on_escape() -> None:
        if state_machine.state == GameState.PAUSED:
            state_machine.change_state(GameState.PLAYING)
        elif state_machine.state == GameState.PLAYING:
            state_machine.change_state(GameState.MENU)

    input_handler.on_grid_click = on_grid_click
    input_handler.on_pause_toggle = on_pause_toggle
    input_handler.on_menu_start = on_menu_start
    input_handler.on_escape = on_escape

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds

        # Process input
        for event in pygame.event.get():
            input_handler.process(event)

            # Menu start on any click
            if (
                state_machine.state == GameState.MENU
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                on_menu_start()

        # Update hover position
        mx, my = input_handler.get_mouse_logical_pos()
        if mx < SCREEN_WIDTH and my < SCREEN_HEIGHT:
            hovered_tile = (mx // 32, my // 32)
        else:
            hovered_tile = None

        # Update logic (if not paused)
        if state_machine.state == GameState.PLAYING:
            # Game logic updates will go here in M2–M4
            pass

        # Render
        renderer.clear()

        if state_machine.state == GameState.MENU:
            renderer.draw_menu()
        else:
            renderer.draw_game(grid, hover_tile=hovered_tile)
            if state_machine.state == GameState.PAUSED:
                renderer.draw_pause_overlay()

        renderer.present()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
