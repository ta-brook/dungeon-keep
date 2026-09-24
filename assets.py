"""Asset loading and sprite registry."""

import glob
import json
import os
from typing import Dict, List, Optional

import pygame


class AssetRegistry:
    """Central registry for all game assets.

    Loads real PNGs when available; skips missing files.
    """

    def __init__(self, manifest_path: str = "assets/manifest.json") -> None:
        self._surfaces: Dict[str, pygame.Surface] = {}
        self._manifest: Dict = {}
        self._manifest_path = manifest_path
        self._floor_variants: List[pygame.Surface] = []
        self._dungeon_master: Optional[pygame.Surface] = None

    def load_all(self) -> None:
        """Load all assets from the manifest; skip missing files."""
        with open(self._manifest_path, "r", encoding="utf-8") as f:
            self._manifest = json.load(f)

        for category_name, category_data in self._manifest["categories"].items():
            base_path = category_data["path"]
            for item in category_data["items"]:
                asset_id = item["id"]
                file_path = os.path.join(base_path, item["file"])

                if os.path.exists(file_path):
                    try:
                        surface = pygame.image.load(file_path).convert_alpha()
                        self._surfaces[asset_id] = surface
                    except Exception as e:
                        print(f"Warning: could not load {file_path}: {e}")
                # If file doesn't exist, skip it (no placeholders)

        # Load user's custom assets
        self._load_floor_variants()
        self._load_dungeon_master()

    def _load_floor_variants(self) -> None:
        """Load dungeon-v1 floor tile variations."""
        pattern = "assets/tiles/dungeon-v1/**/rotations/*.png"
        paths = glob.glob(pattern, recursive=True)
        
        for path in sorted(paths):
            try:
                surf = pygame.image.load(path).convert_alpha()
                # Scale to 32x32 to match grid
                scaled = pygame.transform.scale(surf, (32, 32))
                self._floor_variants.append(scaled)
            except Exception as e:
                print(f"Warning: could not load floor variant {path}: {e}")

        if not self._floor_variants:
            print("Warning: no floor variants found")

    def _load_dungeon_master(self) -> None:
        """Load dungeon master sprite (south-facing idle)."""
        dm_path = "assets/units/male_dungeon_master_half-Idle/Idle/rotations/south.png"
        if os.path.exists(dm_path):
            try:
                surf = pygame.image.load(dm_path).convert_alpha()
                # Scale to 32x32 for consistency
                self._dungeon_master = pygame.transform.scale(surf, (32, 32))
            except Exception as e:
                print(f"Warning: could not load dungeon master: {e}")

    def get(self, asset_id: str) -> Optional[pygame.Surface]:
        """Retrieve a loaded asset surface by ID."""
        return self._surfaces.get(asset_id)

    def get_manifest(self) -> Dict:
        """Return the loaded manifest data."""
        return self._manifest

    def get_random_floor(self) -> Optional[pygame.Surface]:
        """Get a random floor tile variation."""
        if self._floor_variants:
            return self._floor_variants[0]  # Use first variant consistently
        return None

    def has_floor_variants(self) -> bool:
        """Return True if floor variants are loaded."""
        return len(self._floor_variants) > 0

    def get_dungeon_master(self) -> Optional[pygame.Surface]:
        """Get the dungeon master sprite."""
        return self._dungeon_master
