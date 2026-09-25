"""Wave definitions and spawning logic."""

from typing import List, Tuple

from constants import GRID_HEIGHT, GRID_WIDTH, SPAWN_INTERVAL, WAVES
from entities import Hero
from grid import Grid


class WaveManager:
    """Manages hero wave spawning."""

    def __init__(self, grid: Grid) -> None:
        self._grid = grid
        self._wave_index = 0
        self._spawn_queue: List[str] = []
        self._spawn_timer = 0.0
        self._wave_cooldown = 0.0
        self._wave_active = False
        self._all_waves_complete = False

    @property
    def current_wave(self) -> int:
        """Current wave number (1-based)."""
        return self._wave_index + 1

    @property
    def total_waves(self) -> int:
        """Total number of waves."""
        return len(WAVES)

    @property
    def all_waves_complete(self) -> bool:
        """Return True if all waves have been spawned."""
        return self._all_waves_complete

    @property
    def wave_active(self) -> bool:
        """Return True if currently spawning a wave."""
        return self._wave_active

    def start_next_wave(self) -> None:
        """Start the next wave if available."""
        if self._wave_index >= len(WAVES):
            self._all_waves_complete = True
            return

        wave_def = WAVES[self._wave_index]
        self._spawn_queue = []
        for hero_type, count in wave_def:
            self._spawn_queue.extend([hero_type] * count)

        # Shuffle spawn order slightly
        random.shuffle(self._spawn_queue)
        self._wave_active = True
        self._spawn_timer = 0.0
        print(f"Wave {self.current_wave} started! {len(self._spawn_queue)} heroes incoming")

    def update(self, dt: float) -> List[Hero]:
        """Update spawn timers and return newly spawned heroes."""
        spawned: List[Hero] = []

        if not self._wave_active:
            # Start first wave automatically, then wait for cooldown
            if self._wave_index == 0 and not self._all_waves_complete:
                self.start_next_wave()
            return spawned

        if not self._spawn_queue:
            # Wave complete
            self._wave_active = False
            self._wave_index += 1
            self._wave_cooldown = 0.0

            if self._wave_index >= len(WAVES):
                self._all_waves_complete = True
                print("All waves complete!")
            else:
                print(f"Wave {self.current_wave - 1} complete! Next wave incoming...")
            return spawned

        self._spawn_timer += dt
        if self._spawn_timer >= SPAWN_INTERVAL:
            self._spawn_timer -= SPAWN_INTERVAL
            hero_type = self._spawn_queue.pop(0)
            spawn_pos = self._get_spawn_position()
            hero = Hero(spawn_pos[0], spawn_pos[1], hero_type)
            spawned.append(hero)
            print(f"Spawned {hero_type} at {spawn_pos}")

        return spawned

    def start_wave_when_ready(self, dt: float, heroes_alive: int) -> None:
        """Auto-start next wave after cooldown if no heroes remain."""
        if self._wave_active or self._all_waves_complete:
            return

        if heroes_alive > 0:
            return

        self._wave_cooldown += dt
        if self._wave_cooldown >= 3.0:  # Short delay between waves
            self.start_next_wave()

    def _get_spawn_position(self) -> Tuple[int, int]:
        """Get the Entrance spawn position."""
        return self._grid.find_entrance()
