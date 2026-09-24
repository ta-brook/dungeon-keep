"""Asset loading and sprite registry."""

import json
import os
from typing import Dict, Optional

import pygame


class AssetRegistry:
    """Central registry for all game assets.

    Loads real PNGs when available; generates placeholder colored squares
    from manifest.json otherwise.
    """

    def __init__(self, manifest_path: str = "assets/manifest.json") -> None:
        self._surfaces: Dict[str, pygame.Surface] = {}
        self._manifest: Dict = {}
        self._manifest_path = manifest_path

    def load_all(self) -> None:
        """Load all assets from the manifest; generate placeholders if needed."""
        with open(self._manifest_path, "r", encoding="utf-8") as f:
            self._manifest = json.load(f)

        for category_name, category_data in self._manifest["categories"].items():
            base_path = category_data["path"]
            for item in category_data["items"]:
                asset_id = item["id"]
                file_path = os.path.join(base_path, item["file"])
                width, height = item["size"]
                frames = item.get("frames", 1)

                if os.path.exists(file_path):
                    surface = pygame.image.load(file_path).convert_alpha()
                else:
                    surface = self._generate_placeholder(
                        width, height, frames, item.get("placeholder_color")
                    )
                    # Save placeholder for future reference
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    pygame.image.save(surface, file_path)

                self._surfaces[asset_id] = surface

    def _generate_placeholder(
        self,
        width: int,
        height: int,
        frames: int,
        color: Optional[list] = None,
    ) -> pygame.Surface:
        """Generate a solid-color placeholder sprite sheet."""
        if color is None:
            color = [128, 128, 128]

        sheet_width = width * frames
        surface = pygame.Surface((sheet_width, height), pygame.SRCALPHA)
        surface.fill((*color, 255))

        # Draw a dark border so individual frames are visible
        for i in range(frames):
            rect = pygame.Rect(i * width, 0, width, height)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)

        return surface

    def get(self, asset_id: str) -> Optional[pygame.Surface]:
        """Retrieve a loaded asset surface by ID."""
        return self._surfaces.get(asset_id)

    def get_manifest(self) -> Dict:
        """Return the loaded manifest data."""
        return self._manifest
