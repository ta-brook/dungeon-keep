"""UI elements: buttons, panels, sidebar, and HUD."""

from typing import Callable, List, Optional, Tuple

import pygame

from constants import COLORS, PLAY_AREA_WIDTH, SIDEBAR_WIDTH, SCREEN_HEIGHT, TileType


class Button:
    """A clickable UI button."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Callable[[], None],
        cost: int = 0,
    ) -> None:
        self.rect = rect
        self.text = text
        self.callback = callback
        self.cost = cost
        self.hovered = False
        self.disabled = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a Pygame event. Returns True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and not self.disabled:
                self.callback()
                return True
        return False


class UI:
    """Main UI controller for the sidebar."""

    def __init__(self, build_system) -> None:
        self.build_system = build_system
        self.buttons: List[Button] = []
        self.selected_build: Optional[TileType] = None
        self.on_build_selected: Optional[Callable[[TileType], None]] = None
        self.on_build_cancelled: Optional[Callable[[], None]] = None

        self._font_medium = pygame.font.SysFont("monospace", 14)
        self._font_small = pygame.font.SysFont("monospace", 10)
        self._create_buttons()

    def _create_buttons(self) -> None:
        """Create build buttons in the sidebar."""
        panel_x = PLAY_AREA_WIDTH
        start_y = 80
        btn_w = 100
        btn_h = 40
        gap = 8

        rooms = [
            (TileType.LAIR, "Lair", ROOM_COSTS["LAIR"]),
            (TileType.TRAP_ROOM, "Trap", ROOM_COSTS["TRAP_ROOM"]),
            (TileType.TREASURY, "Treasury", ROOM_COSTS["TREASURY"]),
        ]

        for i, (room_type, name, cost) in enumerate(rooms):
            x = panel_x + 14 + (i % 2) * (btn_w + gap)
            y = start_y + (i // 2) * (btn_h + gap)
            rect = pygame.Rect(x, y, btn_w, btn_h)

            def make_callback(rt: TileType = room_type) -> Callable[[], None]:
                return lambda: self._select_build(rt)

            btn = Button(rect, name, make_callback(), cost=cost)
            self.buttons.append(btn)

    def _select_build(self, room_type: TileType) -> None:
        """Select a room type to build."""
        if self.selected_build == room_type:
            # Deselect if already selected
            self.selected_build = None
            if self.on_build_cancelled:
                self.on_build_cancelled()
        else:
            self.selected_build = room_type
            if self.on_build_selected:
                self.on_build_selected(room_type)

    def cancel_build(self) -> None:
        """Cancel current build selection."""
        self.selected_build = None

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a Pygame event. Returns True if a button was clicked."""
        for btn in self.buttons:
            if btn.handle_event(event):
                return True
        return False

    def update(self) -> None:
        """Update button states based on gold availability."""
        for btn in self.buttons:
            btn.disabled = self.build_system.gold < btn.cost

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the UI sidebar onto the given surface."""
        panel_x = PLAY_AREA_WIDTH

        # Gold display
        gold_text = self._font_medium.render(
            f"GOLD: {self.build_system.gold}", True, COLORS["gold_yellow"]
        )
        surface.blit(gold_text, (panel_x + 10, 10))

        # Income hint
        income_text = self._font_small.render(
            "+1/sec per Treasury", True, COLORS["ui_border"]
        )
        surface.blit(income_text, (panel_x + 10, 30))

        # Divider
        pygame.draw.line(
            surface,
            COLORS["ui_border"],
            (panel_x + 10, 50),
            (panel_x + SIDEBAR_WIDTH - 10, 50),
            1,
        )

        # Build label
        build_label = self._font_medium.render("BUILD", True, COLORS["ui_border"])
        surface.blit(build_label, (panel_x + 10, 58))

        # Buttons
        for btn in self.buttons:
            self._draw_button(surface, btn)

        # Selected indicator
        if self.selected_build:
            name = self.build_system.get_room_name(self.selected_build)
            sel_text = self._font_small.render(
                f"Building: {name} (click grid)", True, COLORS["gold_yellow"]
            )
            surface.blit(sel_text, (panel_x + 10, 180))

    def _draw_button(self, surface: pygame.Surface, btn: Button) -> None:
        """Draw a single button."""
        # Background
        if btn.disabled:
            bg_color = COLORS["stone_gray"]
            border_color = COLORS["ui_border"]
        elif self.selected_build and btn.text == self.build_system.get_room_name(self.selected_build):
            bg_color = COLORS["heart_purple"]
            border_color = COLORS["gold_yellow"]
        elif btn.hovered:
            bg_color = COLORS["wall_gray"]
            border_color = COLORS["gold_yellow"]
        else:
            bg_color = COLORS["wall_gray"]
            border_color = COLORS["ui_border"]

        pygame.draw.rect(surface, bg_color, btn.rect)
        pygame.draw.rect(surface, border_color, btn.rect, 2)

        # Text
        text_color = COLORS["ui_border"] if btn.disabled else COLORS["gold_yellow"]
        name_surf = self._font_medium.render(btn.text, True, text_color)
        name_rect = name_surf.get_rect(centerx=btn.rect.centerx, top=btn.rect.top + 4)
        surface.blit(name_surf, name_rect)

        # Cost
        cost_surf = self._font_small.render(f"{btn.cost}g", True, text_color)
        cost_rect = cost_surf.get_rect(centerx=btn.rect.centerx, top=btn.rect.top + 22)
        surface.blit(cost_surf, cost_rect)


# Import here to avoid circular import at module level
from constants import ROOM_COSTS
