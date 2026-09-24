"""Entry point and main game loop."""

import sys

import pygame

from assets import AssetRegistry
from build_system import BuildSystem
from constants import FPS, SCALE_FACTOR, SCREEN_HEIGHT, SCREEN_WIDTH, GameState, TileType
from game_state import StateMachine
from grid import Grid
from input_handler import InputHandler
from renderer import Renderer
from ui import UI


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
    build_system = BuildSystem(grid)
    ui = UI(build_system)
    renderer = Renderer(screen)
    input_handler = InputHandler()

    # Track hovered tile for highlighting
    hovered_tile: tuple | None = None
    build_valid: bool | None = None

    # Wire up input callbacks
    def on_grid_click(x: int, y: int) -> None:
        """Handle grid clicks for building or selecting."""
        if ui.selected_build:
            # Try to build
            success = build_system.build(x, y, ui.selected_build)
            if success:
                print(f"Built {ui.selected_build.name} at ({x}, {y})")
                ui.cancel_build()
            else:
                print(f"Cannot build {ui.selected_build.name} at ({x}, {y})")
        else:
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
            ui.cancel_build()

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

            # UI events (only in playing/paused)
            if state_machine.is_playing():
                ui.handle_event(event)

        # Update hover position and build validity
        mx, my = input_handler.get_mouse_logical_pos()
        if mx < SCREEN_WIDTH and my < SCREEN_HEIGHT:
            hovered_tile = (mx // 32, my // 32)
            if ui.selected_build and hovered_tile:
                hx, hy = hovered_tile
                build_valid = build_system.can_build(hx, hy, ui.selected_build)
            else:
                build_valid = None
        else:
            hovered_tile = None
            build_valid = None

        # Update logic (if not paused)
        if state_machine.state == GameState.PLAYING:
            build_system.update(dt)
            ui.update()

        # Render
        renderer.clear()

        if state_machine.state == GameState.MENU:
            renderer.draw_menu()
        else:
            renderer.draw_game(grid, ui, hover_tile=hovered_tile, build_valid=build_valid)
            if state_machine.state == GameState.PAUSED:
                renderer.draw_pause_overlay()

        renderer.present()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
