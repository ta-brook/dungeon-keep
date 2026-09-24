"""Room placement validation and economy."""


class BuildSystem:
    """Handles building rooms and recruiting monsters."""

    def __init__(self) -> None:
        pass

    def can_build(self, x: int, y: int, room_type) -> bool:
        """Check if a room can be built at the given location."""
        pass

    def build(self, x: int, y: int, room_type) -> bool:
        """Build a room and deduct gold."""
        pass
