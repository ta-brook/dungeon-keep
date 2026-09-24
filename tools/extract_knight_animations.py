"""Extract knight animations from sprite sheet using auto-detection (PIL only).

Scans the sheet and finds sprite-sized clusters of bright pixels automatically.
"""

import os
from PIL import Image


def extract_sprites_auto(image_path: str, output_dir: str, frame_size: int = 32) -> dict:
    """Extract sprites by detecting bright pixel clusters."""
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # Create mask: True where pixel is bright enough to be a sprite
    sprite_mask = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels[x, y]
            brightness = max(r, g, b)
            is_sprite = (a > 50) and (brightness > 60)
            row.append(is_sprite)
        sprite_mask.append(row)
    
    # Find connected components (clusters of bright pixels)
    visited = [[False] * width for _ in range(height)]
    sprites = []
    
    for y in range(height):
        for x in range(width):
            if sprite_mask[y][x] and not visited[y][x]:
                # Found a new cluster, flood fill to find its bounds
                cluster = []
                stack = [(x, y)]
                visited[y][x] = True
                
                while stack:
                    cx, cy = stack.pop()
                    cluster.append((cx, cy))
                    
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if sprite_mask[ny][nx] and not visited[ny][nx]:
                                visited[ny][nx] = True
                                stack.append((nx, ny))
                
                # Get bounding box
                xs = [p[0] for p in cluster]
                ys = [p[1] for p in cluster]
                bbox = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
                
                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                
                # Filter: sprite should be roughly 15-60 pixels in each dimension
                # and not too many pixels total
                if 15 <= bw <= 60 and 15 <= bh <= 60 and len(cluster) < 3000:
                    sprites.append(bbox)
    
    print(f"Found {len(sprites)} potential sprites")
    
    # Sort sprites by position (top to bottom, left to right)
    sprites.sort(key=lambda b: (b[1], b[0]))
    
    # Group sprites by row (similar y coordinate)
    rows = []
    current_row = []
    last_y = -100
    
    for bbox in sprites:
        if abs(bbox[1] - last_y) > 80:
            if current_row:
                rows.append(current_row)
            current_row = [bbox]
            last_y = bbox[1]
        else:
            current_row.append(bbox)
    
    if current_row:
        rows.append(current_row)
    
    print(f"Grouped into {len(rows)} rows")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract and save each row as an animation
    anim_names = ["idle", "walk", "run", "attack_melee", "attack_ranged", 
                  "hit", "hurt", "death", "block", "cast", "jump"]
    
    extracted = {}
    
    for i, row in enumerate(rows):
        if i >= len(anim_names):
            break
        
        name = anim_names[i]
        print(f"\nRow {i}: {name} - {len(row)} frames")
        
        anim_dir = f"{output_dir}/{name}"
        os.makedirs(anim_dir, exist_ok=True)
        
        frames = []
        for j, bbox in enumerate(row):
            # Extract sprite
            sprite = img.crop(bbox)
            
            # Center in frame_size x frame_size canvas
            canvas = Image.new("RGBA", (frame_size, frame_size), (0, 0, 0, 0))
            
            # Scale if too large
            sw, sh = sprite.size
            if sw > frame_size or sh > frame_size:
                scale = min(frame_size / sw, frame_size / sh)
                sw = max(1, int(sw * scale))
                sh = max(1, int(sh * scale))
                sprite = sprite.resize((sw, sh), Image.NEAREST)
            
            # Center
            x = (frame_size - sprite.size[0]) // 2
            y = (frame_size - sprite.size[1]) // 2
            canvas.paste(sprite, (x, y), sprite)
            
            frame_path = f"{anim_dir}/frame_{j:02d}.png"
            canvas.save(frame_path)
            frames.append(canvas)
        
        # Save sprite sheet
        if frames:
            sheet_width = frame_size * len(frames)
            sprite_sheet = Image.new("RGBA", (sheet_width, frame_size))
            for j, frame in enumerate(frames):
                sprite_sheet.paste(frame, (j * frame_size, 0))
            
            sheet_path = f"{output_dir}/{name}_sheet.png"
            sprite_sheet.save(sheet_path)
            
            extracted[name] = {
                "frames": len(frames),
                "dir": anim_dir,
                "sheet": sheet_path,
            }
    
    return extracted


def main():
    print("Auto-extracting knight animations (PIL only)...")
    print("=" * 50)
    
    extracted = extract_sprites_auto(
        "assets/units/animations/knight-animation.png",
        "assets/units/animations/extracted",
        frame_size=32
    )
    
    print("\n" + "=" * 50)
    print("Extraction complete!")
    for name, info in extracted.items():
        print(f"  {name}: {info['frames']} frames")
    
    # Update main knight sprite to use first walk frame
    walk_dir = "assets/units/animations/extracted/walk"
    if os.path.exists(walk_dir):
        frames = sorted([f for f in os.listdir(walk_dir) if f.endswith(".png")])
        if frames:
            src = os.path.join(walk_dir, frames[0])
            import shutil
            shutil.copy2(src, "assets/units/unit_hero_knight.png")
            print("\nUpdated unit_hero_knight.png with first walk frame")


if __name__ == "__main__":
    main()
