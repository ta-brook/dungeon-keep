"""Entry point and main game loop."""

import sys

import pygame

from assets import AssetRegistry
from build_system import BuildSystem
from combat import update_all_combat
from constants import FPS, SCALE_FACTOR, SCREEN_HEIGHT, SCREEN_WIDTH, GameState, TileType
from entities import Hero, Monster
from game_state import StateMachine
from grid import Grid
from input_handler import InputHandler
from renderer import Renderer
from ui import UI
from waves import WaveManager


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
    wave_manager = WaveManager(grid)

    # Entity lists
    monsters: list[Monster] = []
    heroes: list[Hero] = []

    # Track hovered tile for highlighting
    hovered_tile: tuple | None = None
    build_valid: bool | None = None

    # Wire up input callbacks
    def on_grid_click(x: int, y: int) -> None:
        """Handle grid clicks for building, recruiting, or selecting."""
        tile = grid.get_tile(x, y)

        if ui.recruit_mode and tile == TileType.LAIR:
            # Already handled by recruit buttons, but clicking lair again cancels
            ui.cancel_recruit()
            return

        if tile == TileType.LAIR and not ui.selected_build:
            # Enter recruit mode
            ui.start_recruit_mode(x, y)
            return

        if ui.selected_build:
            # Try to build
            success = build_system.build(x, y, ui.selected_build)
            if success:
                print(f"Built {ui.selected_build.name} at ({x}, {y})")
                ui.cancel_build()
            else:
                print(f"Cannot build {ui.selected_build.name} at ({x}, {y})")
        else:
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
            ui.cancel_recruit()

    def on_recruit(monster_type: str) -> None:
        """Recruit a monster at the selected Lair."""
        if ui.recruit_lair_pos:
            lx, ly = ui.recruit_lair_pos
            monster = build_system.recruit(lx, ly, monster_type)
            if monster:
                monsters.append(monster)
                print(f"Recruited {monster_type} at ({lx}, {ly})")
            else:
                print(f"Cannot recruit {monster_type}")

    input_handler.on_grid_click = on_grid_click
    input_handler.on_pause_toggle = on_pause_toggle
    input_handler.on_menu_start = on_menu_start
    input_handler.on_escape = on_escape
    ui.on_recruit = on_recruit

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

        # Update logic (if not paused and not ended)
        if state_machine.state == GameState.PLAYING:
            # Economy
            build_system.update(dt)
            ui.update()

            # Waves
            new_heroes = wave_manager.update(dt)
            heroes.extend(new_heroes)

            wave_manager.start_wave_when_ready(dt, len([h for h in heroes if h.alive]))

            # Entity updates
            all_entities = monsters + heroes
            for monster in monsters:
                monster.update(dt, grid, all_entities)
            for hero in heroes:
                hero.update(dt, grid, all_entities)

            # Combat
            gold_earned = update_all_combat(monsters, heroes, grid, dt)
            if gold_earned > 0:
                build_system.add_gold(gold_earned)

            # Check win/loss
            heart = grid.find_dungeon_heart()
            for hero in heroes:
                if hero.alive and hero.grid_x == heart[0] and hero.grid_y == heart[1]:
                    # Hero reached the heart
                    state_machine.change_state(GameState.LOSS)
                    print("Dungeon Heart destroyed!")
                    break

            # Check win: all waves complete and no heroes alive
            if wave_manager.all_waves_complete:
                if not any(h.alive for h in heroes):
                    state_machine.change_state(GameState.WIN)
                    print("Victory! All waves defeated!")

        # Render
        renderer.clear()

        if state_machine.state == GameState.MENU:
            renderer.draw_menu()
        else:
            wave_info = f"Wave: {wave_manager.current_wave}/{wave_manager.total_waves}"
            if wave_manager.all_waves_complete:
                wave_info = "All waves complete!"

            renderer.draw_game(
                grid,
                ui,
                monsters,
                heroes,
                hover_tile=hovered_tile,
                build_valid=build_valid,
                wave_info=wave_info,
            )

            if state_machine.state == GameState.PAUSED:
                renderer.draw_pause_overlay()
            elif state_machine.state == GameState.WIN:
                renderer.draw_win_screen()
            elif state_machine.state == GameState.LOSS:
                renderer.draw_loss_screen()

        renderer.present()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
