"""Game entities: monsters, heroes, and projectiles."""


class Entity:
    """Base class for all game entities."""

    def __init__(self) -> None:
        pass

    def update(self, dt: float) -> None:
        """Update entity logic."""
        pass

    def draw(self, surface, camera_offset) -> None:
        """Draw the entity."""
        pass


class Monster(Entity):
    """Player-controlled dungeon monster."""
    pass


class Hero(Entity):
    """Invading hero unit."""
    pass
