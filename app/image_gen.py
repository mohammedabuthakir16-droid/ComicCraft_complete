import asyncio
import hashlib
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

def _clean_and_condense_prompt(raw_prompt: str, art_style: str) -> str:
    """
    Cleans and condenses verbose LLM prompts into a punchy, highly effective
    diffusion prompt under 180 characters to prevent HTTP timeouts and 429 rate-limiting.
    """
    # Remove newlines, brackets, and quotes
    text = raw_prompt.replace("\n", " ").replace('"', '').replace("'", "")
    # Remove duplicate boilerplate phrases
    text = re.sub(r'\b(masterpiece|high resolution|clean bold line art|expressive character emotion|professional coloring|graphic novel quality|high detail)\b', '', text, flags=re.IGNORECASE)
    # Strip excess whitespace
    text = re.sub(r'\s+', ' ', text).strip(', ')
    
    # Keep the most descriptive core (up to 130 chars)
    if len(text) > 130:
        # Cut at word boundary
        text = text[:130].rsplit(' ', 1)[0]
        
    return f"comic book panel art, {text}, {art_style}, detailed line art, masterpiece"

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
    Renders an atmospheric, cinematic graphic novel panel with multi-layer
    scenery silhouettes, chiaroscuro shading, Ben-Day halftone texture,
    and comic typography. Ensures 100% offline reliability.
    """
    seed = int(hashlib.md5(prompt.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)
    
    # Style-specific color palettes
    style_lower = art_style.lower()
    if "dark" in style_lower or "noir" in style_lower:
        sky_top, sky_bottom = (15, 23, 42), (30, 41, 59)
        accent_color = (251, 191, 36) # Amber streetlight
        silhouette_color = (10, 15, 26)
    elif "cyber" in style_lower or "sci-fi" in style_lower:
        sky_top, sky_bottom = (10, 10, 28), (49, 10, 80)
        accent_color = (6, 182, 212) # Cyan neon
        silhouette_color = (5, 5, 15)
    elif "manga" in style_lower or "anime" in style_lower:
        sky_top, sky_bottom = (245, 245, 245), (200, 200, 200)
        accent_color = (220, 38, 38) # Crimson accent
        silhouette_color = (20, 20, 20)
    elif "water" in style_lower or "fantasy" in style_lower:
        sky_top, sky_bottom = (30, 58, 80), (13, 148, 136)
        accent_color = (254, 240, 138) # Starlight gold
        silhouette_color = (10, 30, 40)
    else: # Classic Comic Book
        sky_top, sky_bottom = (29, 78, 216), (239, 68, 68)
        accent_color = (250, 204, 21) # Classic comic yellow
        silhouette_color = (15, 23, 42)

    img = Image.new("RGB", (width, height), sky_top)
    draw = ImageDraw.Draw(img)

    # 1. Atmospheric Gradient Sky
    for y in range(height):
        factor = y / height
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * factor)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * factor)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Dramatic Speed Lines / Light Beams
    center_x, center_y = width // 2, int(height * 0.45)
    num_beams = 16
    for i in range(num_beams):
        if i % 2 == 0:
            angle = (2 * math.pi / num_beams) * i + (rng.random() * 0.1)
            dx = math.cos(angle) * width * 1.5
            dy = math.sin(angle) * height * 1.5
            draw.polygon(
                [(center_x, center_y), (center_x + dx, center_y + dy), (center_x + dx * 0.9, center_y + dy * 0.9)],
                fill=(accent_color[0], accent_color[1], accent_color[2])
            )

    # 3. Soft Celestial Glow / Moon / Light Core
    glow_r = 90
    draw.ellipse(
        [(center_x - glow_r, center_y - glow_r), (center_x + glow_r, center_y + glow_r)],
        fill=accent_color,
        outline=(255, 255, 255),
        width=3
    )

    # 4. Comic Ben-Day Halftone Dots
    for y in range(0, height, 22):
        for x in range(0, width, 22):
            draw.ellipse([(x - 2, y - 2), (x + 2, y + 2)], fill=(255, 255, 255, 40))

    # 5. Dynamic Scenery Silhouettes (City Skyline / Forest Ridge)
    ground_y = int(height * 0.65)
    if "cyber" in style_lower or "noir" in style_lower or "city" in prompt.lower():
        # Skyscraper silhouettes
        cur_x = 0
        while cur_x < width:
            b_width = rng.randint(40, 90)
            b_height = rng.randint(80, 220)
            b_top = ground_y - b_height + 40
            draw.rectangle([(cur_x, b_top), (cur_x + b_width, height)], fill=silhouette_color)
            # Illuminated windows
            for wy in range(b_top + 15, ground_y, 20):
                if rng.random() > 0.4:
                    draw.rectangle([(cur_x + 8, wy), (cur_x + 18, wy + 8)], fill=accent_color)
                if rng.random() > 0.4 and b_width > 40:
                    draw.rectangle([(cur_x + 24, wy), (cur_x + 34, wy + 8)], fill=(255, 255, 255))
            cur_x += b_width + 4
    else:
        # Organic trees / Mountain ridge
        mountain_points = [(0, ground_y)]
        for x in range(0, width + 50, 60):
            y_offset = rng.randint(-35, 35)
            mountain_points.append((x, ground_y + y_offset))
        mountain_points.append((width, height))
        mountain_points.append((0, height))
        draw.polygon(mountain_points, fill=silhouette_color)

    # 6. Hero Silhouette in Foreground
    hero_x, hero_y = int(width * 0.42), int(height * 0.62)
    # Head & ears
    draw.ellipse([(hero_x, hero_y - 45), (hero_x + 36, hero_y - 12)], fill=(0, 0, 0))
    # Cape / shoulders
    draw.polygon([
        (hero_x - 20, hero_y + 60),
        (hero_x + 18, hero_y - 10),
        (hero_x + 56, hero_y + 60)
    ], fill=(0, 0, 0))

    # 7. Action Sound Effect Burst
    if sound_effect:
        badge_text = sound_effect.strip().upper()
        spikes = 12
        r_outer, r_inner = 110, 60
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

async def _fetch_pollinations_image(
    prompt: str,
    seed: int,
    output_path: Path,
    width: int = 800,
    height: int = 600
) -> bool:
    """
    Fetches image from Pollinations AI using turbo model with retry and backoff.
    Never uses &enhance=true to prevent LLM timeouts.
    """
    clean_prompt = prompt.replace("\n", " ").strip()
    encoded = urllib.parse.quote(clean_prompt)
    
    # Try fast models: turbo first, then default
    models = ["turbo", ""]
    for model_name in models:
        model_param = f"&model={model_name}" if model_name else ""
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true{model_param}"
        
        # Up to 2 attempts per model with exponential backoff on 429
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=32.0) as client:
                    res = await client.get(url)
                    if res.status_code == 200 and len(res.content) > 1500:
                        with open(output_path, "wb") as f:
                            f.write(res.content)
                        logger.info(f"Successfully generated image via Pollinations ({model_name or 'default'}) [Size: {len(res.content)} bytes]")
                        return True
                    elif res.status_code == 429:
                        # Rate limit: wait and retry
                        wait_sec = (attempt + 1) * 2.0
                        logger.warning(f"Pollinations 429 rate limit. Backing off for {wait_sec}s...")
                        await asyncio.sleep(wait_sec)
                    else:
                        logger.warning(f"Pollinations returned status {res.status_code} for {model_name}")
                        await asyncio.sleep(1.0)
            except Exception as e:
                logger.warning(f"Pollinations attempt {attempt+1} failed ({type(e).__name__}: {e})")
                await asyncio.sleep(1.5)
                
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
    Generates an image for a specific comic panel.
    Uses optimized Pollinations AI with automatic retries and fallback to
    cinematic graphic novel scene illustration.
    """
    filename = f"{comic_id}_panel_{panel_number}.png"
    output_path = config.OUTPUT_DIR / filename
    
    # Return cached if valid and not forcing regeneration
    if output_path.exists() and not force_regenerate:
        # If existing image is non-empty, use it
        if output_path.stat().st_size > 1500:
            return f"/static/outputs/{filename}"
            
    # Deterministic seed for panel continuity
    seed = int(hashlib.md5(f"{comic_id}_{panel_number}".encode()).hexdigest()[:6], 16)
    condensed_prompt = _clean_and_condense_prompt(prompt, art_style)
    
    # 1. Primary Provider: Pollinations AI
    if config.IMAGE_PROVIDER == "pollinations":
        success = await _fetch_pollinations_image(
            prompt=condensed_prompt,
            seed=seed,
            output_path=output_path,
            width=800,
            height=600
        )
        if success:
            return f"/static/outputs/{filename}"

    # 2. Secondary Provider: HuggingFace if configured
    elif config.IMAGE_PROVIDER == "huggingface" and config.HF_API_KEY:
        try:
            hf_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
            payload = {"inputs": condensed_prompt}
            async with httpx.AsyncClient(timeout=35.0) as client:
                res = await client.post(hf_url, headers=headers, json=payload)
                if res.status_code == 200 and len(res.content) > 1500:
                    with open(output_path, "wb") as f:
                        f.write(res.content)
                    return f"/static/outputs/{filename}"
        except Exception as e:
            logger.warning(f"Hugging Face request failed: {e}")

    # 3. High-Fidelity Procedural Comic Scene Fallback
    logger.info(f"Using atmospheric graphic novel renderer for panel {panel_number}")
    return _generate_procedural_comic_image(
        prompt=prompt,
        panel_title=panel_title,
        sound_effect=sound_effect,
        output_path=output_path,
        art_style=art_style
    )
