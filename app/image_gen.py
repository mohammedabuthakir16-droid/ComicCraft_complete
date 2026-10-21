import asyncio
import hashlib
import io
import logging
import math
import random
import re
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional
import httpx
from PIL import Image, ImageDraw, ImageFont
from app import config

logger = logging.getLogger(__name__)

def _format_diffusion_prompt(raw_prompt: str, art_style: str) -> str:
    """
    Cleans and optimizes the comic panel visual description into a high-impact,
    coherent diffusion prompt that maintains character continuity, composition,
    and visual art style.
    """
    # Remove awkward brackets, newlines, quotes
    clean = raw_prompt.replace("\n", " ").replace('"', '').replace("'", "")
    clean = re.sub(r'\s+', ' ', clean).strip(', ')
    
    # Ensure art style is represented
    style_tag = art_style.strip()
    
    # Cap prompt length cleanly at word boundary to stay within optimal diffusion token budget (around 320 chars)
    if len(clean) > 320:
        clean = clean[:320].rsplit(' ', 1)[0]
        
    return f"comic book panel, {clean}, {style_tag}, sharp clean line art, vibrant comic colors, graphic novel illustration, high resolution masterpiece"

def _detect_scene_elements(prompt: str) -> Dict[str, Any]:
    """Detects scene genre, palette, and silhouettes for procedural rendering."""
    p = prompt.lower()
    
    if any(k in p for k in ("kitchen", "cook", "chef", "bake", "pizza", "food", "restaurant")):
        return {
            "type": "kitchen",
            "sky_top": (45, 25, 20),
            "sky_bottom": (180, 83, 9),
            "accent": (251, 191, 36),
            "silhouette": (25, 15, 10),
            "sound_default": "SIZZLE!"
        }
    elif any(k in p for k in ("space", "galaxy", "orbit", "alien", "planet", "star", "astronaut", "nebula")):
        return {
            "type": "space",
            "sky_top": (10, 10, 30),
            "sky_bottom": (76, 29, 149),
            "accent": (56, 189, 248),
            "silhouette": (5, 5, 20),
            "sound_default": "WHOOSH!"
        }
    elif any(k in p for k in ("detective", "noir", "investigat", "crime", "rain", "alley", "shadow")):
        return {
            "type": "noir",
            "sky_top": (15, 23, 42),
            "sky_bottom": (30, 41, 59),
            "accent": (251, 191, 36),
            "silhouette": (10, 15, 26),
            "sound_default": "DRIP-DROP..."
        }
    elif any(k in p for k in ("cyber", "hack", "neon", "robot", "future", "megacity", "droid")):
        return {
            "type": "cyberpunk",
            "sky_top": (10, 10, 28),
            "sky_bottom": (49, 10, 80),
            "accent": (6, 182, 212),
            "silhouette": (5, 5, 15),
            "sound_default": "SKRRRT..."
        }
    elif any(k in p for k in ("forest", "tree", "wood", "enchanted", "nature", "grove", "fox")):
        return {
            "type": "forest",
            "sky_top": (30, 58, 80),
            "sky_bottom": (13, 148, 136),
            "accent": (254, 240, 138),
            "silhouette": (10, 30, 40),
            "sound_default": "RUSTLE..."
        }
    elif any(k in p for k in ("sea", "ocean", "water", "underwater", "trench", "ship", "pirate")):
        return {
            "type": "ocean",
            "sky_top": (12, 74, 110),
            "sky_bottom": (14, 165, 233),
            "accent": (253, 224, 71),
            "silhouette": (8, 47, 73),
            "sound_default": "SPLASH!"
        }
    elif any(k in p for k in ("wizard", "magic", "castle", "knight", "dragon", "dungeon")):
        return {
            "type": "castle",
            "sky_top": (30, 27, 75),
            "sky_bottom": (126, 34, 206),
            "accent": (250, 204, 21),
            "silhouette": (19, 15, 38),
            "sound_default": "CRACKLE!"
        }
    else:
        return {
            "type": "general",
            "sky_top": (29, 78, 216),
            "sky_bottom": (239, 68, 68),
            "accent": (250, 204, 21),
            "silhouette": (15, 23, 42),
            "sound_default": "POW!"
        }

def _generate_procedural_comic_image(
    prompt: str,
    panel_title: str,
    sound_effect: str,
    output_path: Path,
    art_style: str = "Classic Comic Book",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Renders an atmospheric, cinematic graphic novel panel with prompt-specific
    scenery silhouettes, chiaroscuro shading, Ben-Day halftone texture,
    and comic typography. Ensures 100% offline reliability.
    """
    seed = int(hashlib.md5(f"{prompt}_{panel_title}".encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)
    
    scene = _detect_scene_elements(prompt)
    sky_top = scene["sky_top"]
    sky_bottom = scene["sky_bottom"]
    accent_color = scene["accent"]
    silhouette_color = scene["silhouette"]
    active_sound = sound_effect.strip() if sound_effect else scene["sound_default"]

    img = Image.new("RGB", (width, height), sky_top)
    draw = ImageDraw.Draw(img)

    # 1. Atmospheric Gradient Sky
    for y in range(height):
        factor = y / height
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * factor)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * factor)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Dramatic Light Beams / Speed Lines
    center_x, center_y = width // 2, int(height * 0.45)
    num_beams = 16
    for i in range(num_beams):
        if i % 2 == 0:
            angle = (2 * math.pi / num_beams) * i + (rng.random() * 0.08)
            dx = math.cos(angle) * width * 1.5
            dy = math.sin(angle) * height * 1.5
            draw.polygon(
                [(center_x, center_y), (center_x + dx, center_y + dy), (center_x + dx * 0.9, center_y + dy * 0.9)],
                fill=accent_color
            )

    # 3. Soft Celestial Core / Lamp / Moon
    glow_r = 75
    draw.ellipse(
        [(center_x - glow_r, center_y - glow_r), (center_x + glow_r, center_y + glow_r)],
        fill=accent_color,
        outline=(255, 255, 255),
        width=3
    )

    # 4. Comic Ben-Day Halftone Dots
    for y in range(0, height, 24):
        for x in range(0, width, 24):
            draw.ellipse([(x - 2, y - 2), (x + 2, y + 2)], fill=(255, 255, 255, 30))

    # 5. Dynamic Scenery Silhouettes Based on Prompt Theme
    ground_y = int(height * 0.65)
    s_type = scene["type"]
    
    if s_type in ("cyberpunk", "noir"):
        # Skyscraper silhouettes with illuminated windows
        cur_x = 0
        while cur_x < width:
            b_width = rng.randint(45, 95)
            b_height = rng.randint(90, 240)
            b_top = ground_y - b_height + 40
            draw.rectangle([(cur_x, b_top), (cur_x + b_width, height)], fill=silhouette_color)
            for wy in range(b_top + 15, ground_y, 22):
                if rng.random() > 0.4:
                    draw.rectangle([(cur_x + 8, wy), (cur_x + 18, wy + 8)], fill=accent_color)
                if rng.random() > 0.4 and b_width > 45:
                    draw.rectangle([(cur_x + 24, wy), (cur_x + 34, wy + 8)], fill=(255, 255, 255))
            cur_x += b_width + 4
    elif s_type == "space":
        # Planetary horizon and distant celestial bodies
        draw.arc([(center_x - 220, ground_y - 80), (center_x + 220, ground_y + 360)], 0, 180, fill=accent_color, width=4)
        for _ in range(35):
            sx, sy = rng.randint(0, width), rng.randint(0, ground_y)
            draw.ellipse([(sx, sy), (sx + 3, sy + 3)], fill=(255, 255, 255))
        # Surface terrain
        terrain_points = [(0, ground_y)]
        for x in range(0, width + 50, 50):
            terrain_points.append((x, ground_y + rng.randint(-15, 25)))
        terrain_points.append((width, height))
        terrain_points.append((0, height))
        draw.polygon(terrain_points, fill=silhouette_color)
    elif s_type == "kitchen":
        # Countertops, hanging utensils, and warm kitchen frames
        draw.rectangle([(0, ground_y), (width, height)], fill=silhouette_color)
        draw.rectangle([(width // 4, ground_y - 70), (width // 4 + 80, ground_y)], fill=accent_color)
        draw.rectangle([(3 * width // 4 - 60, ground_y - 90), (3 * width // 4 + 40, ground_y)], fill=(255, 255, 255))
    elif s_type == "ocean":
        # Crashing rolling waves
        wave_points = [(0, ground_y)]
        for x in range(0, width + 40, 40):
            wave_points.append((x, ground_y + int(math.sin(x * 0.05) * 20)))
        wave_points.append((width, height))
        wave_points.append((0, height))
        draw.polygon(wave_points, fill=silhouette_color)
    else:
        # Organic trees / Mountain ridge
        mountain_points = [(0, ground_y)]
        for x in range(0, width + 50, 60):
            y_offset = rng.randint(-35, 35)
            mountain_points.append((x, ground_y + y_offset))
        mountain_points.append((width, height))
        mountain_points.append((0, height))
        draw.polygon(mountain_points, fill=silhouette_color)

    # 6. Hero Dynamic Silhouette in Foreground
    hero_x, hero_y = int(width * 0.44), int(height * 0.60)
    draw.ellipse([(hero_x, hero_y - 45), (hero_x + 36, hero_y - 12)], fill=(0, 0, 0))
    draw.polygon([
        (hero_x - 22, hero_y + 65),
        (hero_x + 18, hero_y - 10),
        (hero_x + 58, hero_y + 65)
    ], fill=(0, 0, 0))

    # 7. Action Sound Effect Burst
    if active_sound:
        badge_text = active_sound.strip().upper()
        spikes = 12
        r_outer, r_inner = 105, 55
        s_cx, s_cy = width - 110, 85
        points = []
        for i in range(spikes * 2):
            r = r_outer if i % 2 == 0 else r_inner
            theta = (math.pi / spikes) * i
            points.append((s_cx + r * math.cos(theta), s_cy + r * math.sin(theta)))
        draw.polygon(points, fill=(239, 68, 68), outline=(0, 0, 0))
        
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        draw.text((s_cx - 28, s_cy - 8), badge_text, fill=(255, 255, 255), font=font)

    # 8. Crisp Comic Outer Frame
    draw.rectangle([(6, 6), (width - 6, height - 6)], outline=(0, 0, 0), width=8)
    draw.rectangle([(12, 12), (width - 12, height - 12)], outline=(255, 255, 255), width=2)

    # 9. Bottom Panel Title Banner
    banner_height = 42
    draw.rectangle([(14, height - banner_height - 14), (width - 14, height - 14)], fill=(15, 23, 42))
    draw.text((28, height - banner_height - 8), f"★ {panel_title} ★", fill=(255, 255, 255))

    img.save(output_path, "PNG")
    return f"/static/outputs/{output_path.name}"

async def _generate_pollinations_diffusion(
    prompt: str,
    seed: int,
    output_path: Path,
    width: int = 800,
    height: int = 600
) -> bool:
    """
    Primary AI Image Generation:
    Invokes Pollinations text-to-image diffusion models with prompt engineering.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    endpoints = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model=turbo"
    ]
    
    headers = {
        "User-Agent": "ComicCraft-Studio/2.0 (Macintosh; Comic AI Director)"
    }
    
    for url in endpoints:
        try:
            async with httpx.AsyncClient(timeout=14.0, follow_redirects=True) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200 and len(res.content) > 3000:
                    # Convert to RGB image and ensure correct dimensions
                    with Image.open(io.BytesIO(res.content)) as im:
                        rgb = im.convert("RGB")
                        resized = rgb.resize((width, height), Image.Resampling.LANCZOS)
                        resized.save(output_path, format="PNG", optimize=True)
                        logger.info(f"Generated authentic comic diffusion image: {output_path.name} ({len(res.content)} bytes)")
                        return True
        except Exception as e:
            logger.warning(f"Pollinations diffusion attempt failed for {url[:50]}...: {e}")
            
    return False

async def generate_panel_image(
    prompt: str,
    comic_id: str,
    panel_number: int,
    panel_title: str = "Panel",
    sound_effect: str = "",
    art_style: str = "Classic Comic Book",
    force_regenerate: bool = False
) -> str:
    """
    Generates high-quality comic panel art faithful to the prompt:
    1. Primary: Genuine AI Text-to-Image Diffusion Model (Pollinations).
    2. Fallback: Prompt-Aware Procedural Graphic Novel Renderer.
    """
    filename = f"{comic_id}_panel_{panel_number}.png"
    output_path = config.OUTPUT_DIR / filename
    
    # Return cached if valid and not forcing regeneration
    if output_path.exists() and not force_regenerate:
        if output_path.stat().st_size > 1500:
            return f"/static/outputs/{filename}"
            
    # Deterministic seed for panel visual continuity
    seed = int(hashlib.md5(f"{comic_id}_{panel_number}".encode()).hexdigest()[:6], 16)
    diffusion_prompt = _format_diffusion_prompt(prompt, art_style)
    
    # 1. Primary Engine: AI Diffusion Image Generation
    success = await _generate_pollinations_diffusion(
        prompt=diffusion_prompt,
        seed=seed,
        output_path=output_path,
        width=800,
        height=600
    )
    if success:
        return f"/static/outputs/{filename}"

    # 2. Secondary Engine: Prompt-Aware Atmospheric Comic Renderer
    logger.info(f"Using atmospheric graphic novel renderer for panel {panel_number}")
    return _generate_procedural_comic_image(
        prompt=prompt,
        panel_title=panel_title,
        sound_effect=sound_effect,
        output_path=output_path,
        art_style=art_style
    )
