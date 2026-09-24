"""UI elements: buttons, panels, sidebar, and HUD."""

from typing import Callable, List, Optional, Tuple

import pygame

from assets import AssetRegistry
from constants import COLORS, MONSTER_COSTS, PLAY_AREA_WIDTH, SIDEBAR_WIDTH, SCREEN_HEIGHT, TileType


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
        self.pressed = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a Pygame event. Returns True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and not self.disabled:
                self.pressed = True
                self.callback()
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

        return False


class UI:
    """Main UI controller for the sidebar."""

    def __init__(self, build_system, assets: AssetRegistry) -> None:
        self.build_system = build_system
        self._assets = assets
        self.buttons: List[Button] = []
        self.selected_build: Optional[TileType] = None
        self.on_build_selected: Optional[Callable[[TileType], None]] = None
        self.on_build_cancelled: Optional[Callable[[], None]] = None

        # Recruitment mode
        self.recruit_mode = False
        self.recruit_lair_pos: Optional[Tuple[int, int]] = None
        self.recruit_buttons: List[Button] = []
        self.on_recruit: Optional[Callable[[str], None]] = None

        self._font_medium = pygame.font.SysFont("monospace", 14)
        self._font_small = pygame.font.SysFont("monospace", 10)
        self._create_build_buttons()
        self._create_recruit_buttons()

    def _create_build_buttons(self) -> None:
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

    def _create_recruit_buttons(self) -> None:
        """Create recruit buttons for when a Lair is selected."""
        panel_x = PLAY_AREA_WIDTH
        start_y = 200
        btn_w = 80
        btn_h = 30
        gap = 6

        monsters = [
            ("goblin", "Goblin", MONSTER_COSTS["goblin"]),
            ("slime", "Slime", MONSTER_COSTS["slime"]),
            ("skeleton", "Skeleton", MONSTER_COSTS["skeleton"]),
        ]

        for i, (mtype, name, cost) in enumerate(monsters):
            x = panel_x + 14 + (i % 2) * (btn_w + gap)
            y = start_y + (i // 2) * (btn_h + gap)
            rect = pygame.Rect(x, y, btn_w, btn_h)

            def make_callback(mt: str = mtype) -> Callable[[], None]:
                return lambda: self._do_recruit(mt)

            btn = Button(rect, name, make_callback(), cost=cost)
            self.recruit_buttons.append(btn)

    def _select_build(self, room_type: TileType) -> None:
        """Select a room type to build."""
        if self.selected_build == room_type:
            self.selected_build = None
            if self.on_build_cancelled:
                self.on_build_cancelled()
        else:
            self.selected_build = room_type
            self.recruit_mode = False
            if self.on_build_selected:
                self.on_build_selected(room_type)

    def start_recruit_mode(self, lair_x: int, lair_y: int) -> None:
        """Enter recruit mode for a specific Lair."""
        self.recruit_mode = True
        self.recruit_lair_pos = (lair_x, lair_y)
        self.selected_build = None

    def cancel_recruit(self) -> None:
        """Exit recruit mode."""
        self.recruit_mode = False
        self.recruit_lair_pos = None

    def _do_recruit(self, monster_type: str) -> None:
        """Handle recruit button click."""
        if self.on_recruit:
            self.on_recruit(monster_type)
        self.recruit_mode = False
        self.recruit_lair_pos = None

    def cancel_build(self) -> None:
        """Cancel current build selection."""
        self.selected_build = None
        self.recruit_mode = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a Pygame event. Returns True if a button was clicked."""
        if self.recruit_mode:
            for btn in self.recruit_buttons:
                if btn.handle_event(event):
                    return True
            # Clicking outside cancels recruit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.cancel_recruit()
                return True

        for btn in self.buttons:
            if btn.handle_event(event):
                return True
        return False

    def update(self) -> None:
        """Update button states based on gold availability."""
        for btn in self.buttons:
            btn.disabled = self.build_system.gold < btn.cost

        for btn in self.recruit_buttons:
            btn.disabled = self.build_system.gold < btn.cost

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the UI sidebar onto the given surface."""
        panel_x = PLAY_AREA_WIDTH

        # Draw panel background
        panel_surf = self._assets.get("panel")
        if panel_surf:
            surface.blit(panel_surf, (panel_x, 0))
        else:
            panel_rect = pygame.Rect(panel_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
            pygame.draw.rect(surface, COLORS["wall_gray"], panel_rect)
            pygame.draw.rect(surface, COLORS["ui_border"], panel_rect, 2)

        # Gold icon + display
        gold_icon = self._assets.get("gold_icon")
        if gold_icon:
            surface.blit(gold_icon, (panel_x + 10, 10))
            gold_x = panel_x + 30
        else:
            gold_x = panel_x + 10

        gold_text = self._font_medium.render(
            f"{self.build_system.gold}", True, COLORS["gold_yellow"]
        )
        surface.blit(gold_text, (gold_x, 10))

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

        # Build buttons
        for btn in self.buttons:
            self._draw_button(surface, btn)

        # Selected indicator
        if self.selected_build:
            name = self.build_system.get_room_name(self.selected_build)
            sel_text = self._font_small.render(
                f"Building: {name} (click grid)", True, COLORS["gold_yellow"]
            )
            surface.blit(sel_text, (panel_x + 10, 180))

        # Recruit mode
        if self.recruit_mode and self.recruit_lair_pos:
            rec_label = self._font_medium.render("RECRUIT", True, COLORS["slime_green"])
            surface.blit(rec_label, (panel_x + 10, 185))

            for btn in self.recruit_buttons:
                self._draw_button(surface, btn)

    def _draw_button(self, surface: pygame.Surface, btn: Button) -> None:
        """Draw a single button using sprite assets."""
        # Determine sprite state
        if btn.disabled:
            sprite_id = "button_disabled"
        elif btn.pressed:
            sprite_id = "button_pressed"
        elif btn.hovered:
            sprite_id = "button_hover"
        else:
            sprite_id = "button_default"

        btn_surf = self._assets.get(sprite_id)
        if btn_surf:
            # Scale button sprite to match button rect
            scaled = pygame.transform.scale(btn_surf, (btn.rect.width, btn.rect.height))
            surface.blit(scaled, btn.rect)
        else:
            # Fallback to rectangle
            bg_color = COLORS["stone_gray"] if btn.disabled else COLORS["wall_gray"]
            border_color = COLORS["ui_border"] if btn.disabled else COLORS["gold_yellow"] if btn.hovered else COLORS["ui_border"]
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
