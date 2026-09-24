"""Extract sprites from art sheets and integrate into game.

This script:
1. Deletes glitched placeholder PNGs
2. Auto-extracts sprites from art1.png and art2.png
3. Saves key sprites to correct asset folders
4. Updates asset registry
"""

import os
import shutil
from PIL import Image

# ============================================================================
# STEP 1: Delete glitched placeholder files
# ============================================================================

def delete_placeholders() -> None:
    """Delete tiny placeholder PNGs that cause visual glitches."""
    placeholder_dirs = [
        "assets/tiles",
        "assets/units",
        "assets/ui",
        "assets/effects",
    ]
    
    deleted = 0
    for directory in placeholder_dirs:
        if not os.path.exists(directory):
            continue
        for filename in os.listdir(directory):
            if not filename.endswith(".png"):
                continue
            filepath = os.path.join(directory, filename)
            size = os.path.getsize(filepath)
            # Delete tiny files (< 300 bytes = placeholders)
            if size < 300:
                os.remove(filepath)
                deleted += 1
                print(f"Deleted placeholder: {filepath} ({size} bytes)")
    
    print(f"\nDeleted {deleted} placeholder files")


# ============================================================================
# STEP 2: Auto-extract sprites from sheets
# ============================================================================

def find_sprites_auto(image_path: str, min_size: int = 20, bg_mode: str = "transparent") -> list:
    """Find sprite bounding boxes using flood-fill on non-background pixels.
    
    bg_mode: 'transparent' for alpha, 'black' for black background
    """
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    visited = [[False] * width for _ in range(height)]
    sprites = []
    
    def is_sprite_pixel(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        if bg_mode == "transparent":
            return a > 30
        else:  # black background
            return r > 30 or g > 30 or b > 30
    
    def flood_fill(start_x: int, start_y: int) -> tuple:
        stack = [(start_x, start_y)]
        visited[start_y][start_x] = True
        min_x, min_y = start_x, start_y
        max_x, max_y = start_x, start_y
        
        while stack:
            x, y = stack.pop()
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                    if is_sprite_pixel(nx, ny):
                        visited[ny][nx] = True
                        stack.append((nx, ny))
        
        return (min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
    
    for y in range(height):
        for x in range(width):
            if not visited[y][x] and is_sprite_pixel(x, y):
                bbox = flood_fill(x, y)
                if bbox[2] >= min_size and bbox[3] >= min_size:
                    sprites.append(bbox)
    
    return sprites


def extract_and_save(image_path: str, output_dir: str, prefix: str, bg_mode: str = "transparent") -> list:
    """Extract all sprites from an image and save them."""
    img = Image.open(image_path).convert("RGBA")
    sprites = find_sprites_auto(image_path, min_size=20, bg_mode=bg_mode)
    
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    
    for i, (x, y, w, h) in enumerate(sprites):
        sprite = img.crop((x, y, x + w, y + h))
        path = os.path.join(output_dir, f"{prefix}_{i:03d}_{w}x{h}.png")
        sprite.save(path)
        saved.append(path)
    
    return saved


# ============================================================================
# STEP 3: Manual crop key sprites from art2.png (cleaner sheet)
# ============================================================================

def extract_key_sprites_art2() -> dict:
    """Extract known sprites from art2.png using manual coordinates."""
    img = Image.open("assets/arts/dungeon-keep-art2.png").convert("RGBA")
    
    # Define crop regions (x, y, w, h) based on visual inspection
    # These are approximate and may need tuning
    crops = {
        # Characters
        "unit_goblin_idle": (30, 70, 130, 170),
        "unit_slime_idle": (200, 70, 130, 170),
        "unit_skeleton_idle": (370, 70, 130, 170),
        "unit_hero_knight": (540, 70, 130, 170),
        "unit_hero_paladin": (710, 70, 130, 170),
        
        # Dungeon Heart
        "tile_dungeon_heart": (1140, 30, 300, 280),
        
        # Tiles
        "tile_stone_floor": (25, 390, 90, 90),
        "tile_stone_wall": (415, 390, 90, 90),
        "tile_lair": (25, 590, 100, 100),  # Chest as lair
        "tile_trap_room": (545, 590, 100, 100),  # Trap prop
        "tile_treasury": (25, 590, 100, 100),  # Reuse chest
        
        # Items
        "ui_gold_icon": (725, 800, 70, 70),
        
        # Effects
        "effect_damage": (930, 960, 130, 70),  # Blood
        "effect_death": (200, 960, 130, 70),  # Explosion
    }
    
    output_dir = "assets/extracted"
    os.makedirs(output_dir, exist_ok=True)
    
    extracted = {}
    for name, (x, y, w, h) in crops.items():
        # Ensure crop is within image bounds
        x = max(0, x)
        y = max(0, y)
        w = min(w, img.width - x)
        h = min(h, img.height - y)
        
        sprite = img.crop((x, y, x + w, y + h))
        path = os.path.join(output_dir, f"{name}.png")
        sprite.save(path)
        extracted[name] = path
        print(f"Extracted: {name} ({w}x{h}) -> {path}")
    
    return extracted


# ============================================================================
# STEP 4: Copy enemy knight to units folder
# ============================================================================

def copy_enemy_knight() -> None:
    """Copy enemy knight south-facing sprite to units folder."""
    src = "assets/units/3232_pixel-art_enemy_kni-Idle/Idle/rotations/south.png"
    dst = "assets/units/unit_hero_knight.png"
    
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied enemy knight -> {dst}")
    
    # Also copy other directions if we want them later
    directions = ["south", "south-east", "east", "north-east", 
                  "north", "north-west", "west", "south-west"]
    for direction in directions:
        src_path = f"assets/units/3232_pixel-art_enemy_kni-Idle/Idle/rotations/{direction}.png"
        if os.path.exists(src_path):
            dst_path = f"assets/units/unit_hero_knight_{direction}.png"
            shutil.copy2(src_path, dst_path)


# ============================================================================
# STEP 5: Scale sprites to game size
# ============================================================================

def scale_sprite(input_path: str, output_path: str, size: tuple) -> None:
    """Scale a sprite to target size using nearest neighbor."""
    img = Image.open(input_path).convert("RGBA")
    scaled = img.resize(size, Image.NEAREST)
    scaled.save(output_path)
    print(f"Scaled: {input_path} -> {output_path} ({size[0]}x{size[1]})")


def scale_key_sprites() -> None:
    """Scale extracted sprites to game-appropriate sizes."""
    extracted_dir = "assets/extracted"
    
    # Unit sprites -> 32x32
    unit_sprites = ["unit_goblin_idle", "unit_slime_idle", "unit_skeleton_idle",
                    "unit_hero_knight", "unit_hero_paladin"]
    for name in unit_sprites:
        src = os.path.join(extracted_dir, f"{name}.png")
        if os.path.exists(src):
            scale_sprite(src, f"assets/units/{name}.png", (32, 32))
    
    # Tile sprites -> 32x32
    tile_sprites = ["tile_stone_floor", "tile_stone_wall", "tile_dungeon_heart",
                    "tile_lair", "tile_trap_room", "tile_treasury"]
    for name in tile_sprites:
        src = os.path.join(extracted_dir, f"{name}.png")
        if os.path.exists(src):
            scale_sprite(src, f"assets/tiles/{name}.png", (32, 32))
    
    # UI icons -> 16x16
    if os.path.exists(os.path.join(extracted_dir, "ui_gold_icon.png")):
        scale_sprite(os.path.join(extracted_dir, "ui_gold_icon.png"), 
                     "assets/ui/ui_gold_icon.png", (16, 16))
    
    # Effects -> 16x16 or 32x32
    if os.path.exists(os.path.join(extracted_dir, "effect_damage.png")):
        scale_sprite(os.path.join(extracted_dir, "effect_damage.png"),
                     "assets/effects/effect_damage.png", (16, 16))
    if os.path.exists(os.path.join(extracted_dir, "effect_death.png")):
        scale_sprite(os.path.join(extracted_dir, "effect_death.png"),
                     "assets/effects/effect_death.png", (32, 32))


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("Dungeon Keep Asset Integration Tool")
    print("=" * 60)
    
    print("\n[1/5] Deleting glitched placeholder files...")
    delete_placeholders()
    
    print("\n[2/5] Extracting key sprites from art2.png...")
    extract_key_sprites_art2()
    
    print("\n[3/5] Copying enemy knight sprite...")
    copy_enemy_knight()
    
    print("\n[4/5] Scaling sprites to game size...")
    scale_key_sprites()
    
    print("\n[5/5] Done!")
    print("\nNew assets ready in:")
    print("  - assets/tiles/")
    print("  - assets/units/")
    print("  - assets/ui/")
    print("  - assets/effects/")
    print("\nRun 'python main.py' to see the new sprites in-game!")


if __name__ == "__main__":
    main()
