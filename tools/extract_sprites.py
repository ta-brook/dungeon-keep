"""Sprite sheet extraction tool.

Extracts individual sprites from sprite sheets by detecting non-background
pixel regions. Saves extracted sprites to assets/extracted/.
"""

import os
import sys

import pygame


def find_sprites(surface: pygame.Surface, bg_threshold: int = 10) -> list:
    """Find sprite bounding boxes in a surface.

    For transparent images: detects non-transparent regions.
    For black-bg images: detects non-black regions.
    """
    width, height = surface.get_size()
    pixels = pygame.surfarray.array3d(surface)
    alpha = None
    try:
        alpha = pygame.surfarray.array_alpha(surface)
    except Exception:
        pass

    visited = [[False] * width for _ in range(height)]
    sprites = []

    def bfs(start_x: int, start_y: int) -> tuple:
        """Find bounding box of connected non-background pixels."""
        queue = [(start_x, start_y)]
        visited[start_y][start_x] = True
        min_x, min_y = start_x, start_y
        max_x, max_y = start_x, start_y

        while queue:
            x, y = queue.pop(0)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                    if is_sprite_pixel(nx, ny, pixels, alpha, bg_threshold):
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        return (min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

    def is_sprite_pixel(x: int, y: int, px, a, threshold: int) -> bool:
        """Check if pixel is part of a sprite (not background)."""
        if a is not None:
            return a[y][x] > threshold
        # For black background images
        r, g, b = px[y][x]
        return r > threshold or g > threshold or b > threshold

    for y in range(height):
        for x in range(width):
            if not visited[y][x] and is_sprite_pixel(x, y, pixels, alpha, bg_threshold):
                bbox = bfs(x, y)
                # Filter out tiny noise regions
                if bbox[2] >= 8 and bbox[3] >= 8:
                    sprites.append(bbox)

    return sprites


def extract_sprite(surface: pygame.Surface, bbox: tuple) -> pygame.Surface:
    """Extract a sprite region from a surface."""
    x, y, w, h = bbox
    rect = pygame.Rect(x, y, w, h)
    extracted = pygame.Surface((w, h), pygame.SRCALPHA)
    extracted.blit(surface, (0, 0), rect)
    return extracted


def save_sprites(sheet_path: str, output_dir: str, prefix: str = "sprite") -> list:
    """Extract and save all sprites from a sheet."""
    pygame.init()
    surface = pygame.image.load(sheet_path).convert_alpha()
    
    sprites = find_sprites(surface)
    print(f"Found {len(sprites)} sprites in {sheet_path}")

    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []

    for i, bbox in enumerate(sprites):
        sprite = extract_sprite(surface, bbox)
        path = os.path.join(output_dir, f"{prefix}_{i:03d}.png")
        pygame.image.save(sprite, path)
        saved_paths.append(path)
        print(f"  Saved: {path} ({bbox[2]}x{bbox[3]})")

    return saved_paths


def main() -> None:
    """Extract sprites from all art sheets."""
    # Extract from art1.png (transparent, comprehensive sheet)
    if os.path.exists("assets/arts/dungeon-keep-art1.png"):
        print("\n=== Extracting from art1.png ===")
        save_sprites("assets/arts/dungeon-keep-art1.png", "assets/extracted/art1", "art1")

    # Extract from art2.png (black background, clean sheet)
    if os.path.exists("assets/arts/dungeon-keep-art2.png"):
        print("\n=== Extracting from art2.png ===")
        save_sprites("assets/arts/dungeon-keep-art2.png", "assets/extracted/art2", "art2")

    print("\nDone! Review extracted sprites in assets/extracted/")


if __name__ == "__main__":
    main()
