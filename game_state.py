"""Game state machine and high-level flow control."""

from constants import GameState


class StateMachine:
    """Manages transitions between game states."""

    def __init__(self, initial_state: GameState = GameState.MENU) -> None:
        self._state = initial_state
        self._previous_state: GameState = initial_state

    @property
    def state(self) -> GameState:
        """Current game state."""
        return self._state

    @property
    def previous_state(self) -> GameState:
        """Previous game state before the most recent transition."""
        return self._previous_state

    def change_state(self, new_state: GameState) -> None:
        """Transition to a new state."""
        self._previous_state = self._state
        self._state = new_state

    def is_playing(self) -> bool:
        """Return True if currently in PLAYING or PAUSED state."""
        return self._state in {GameState.PLAYING, GameState.PAUSED}
