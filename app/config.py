import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = STATIC_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "images").mkdir(parents=True, exist_ok=True)

# Load environment
load_dotenv(BASE_DIR / ".env")

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TEXT_MODEL = os.getenv("TEXT_MODEL", "gemini-2.5-flash").strip()
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "pollinations").strip().lower()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# Comic art styles supported
SUPPORTED_STYLES = [
    {"id": "classic-comic", "name": "Classic Comic Book", "prompt_suffix": "vintage 1980s American comic book style, bold ink lines, dynamic superhero comic coloring, halftone dots"},
    {"id": "manga", "name": "Manga / Anime", "prompt_suffix": "Japanese shonen manga style, crisp anime ink illustration, expressive cinematic action, vibrant cel shading"},
    {"id": "graphic-novel", "name": "Dark Graphic Novel", "prompt_suffix": "dark graphic novel noir style, dramatic chiaroscuro shadows, high contrast, gritty detailed line art"},
    {"id": "cyberpunk", "name": "Cyberpunk Sci-Fi", "prompt_suffix": "cyberpunk comic art, neon glow, futuristic tech details, vivid holographic palette, stylized ink outlines"},
    {"id": "watercolor", "name": "Indie Watercolor Comic", "prompt_suffix": "hand-drawn indie comic watercolor painting, whimsical delicate ink contours, soft color washes, storybook aesthetic"},
    {"id": "retro-pop", "name": "Retro Pop Art", "prompt_suffix": "1960s Pop Art comic style, Roy Lichtenstein aesthetic, bold primary colors, heavy Ben-Day dots, punchy outlines"}
]

# Character archetypes and story genres
STORY_GENRES = ["Superhero Adventure", "Sci-Fi Odyssey", "Fantasy Quest", "Cyberpunk Mystery", "Comedy Strip", "Historical Legend"]
