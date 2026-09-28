import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from run import app
from app import config
from app.gemini_api import generate_comic_story
from app.panel_gen import process_comic_panels
from app.layout import calculate_panel_layout
from app.image_gen import generate_panel_image
from app.pdf_export import export_comic_to_pdf

client = TestClient(app)

def test_health_check():
    """Verify health endpoint returns 200 OK and valid status."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "ComicCraft" in data["app"]

def test_home_page():
    """Verify home page loads HTML with comic studio components."""
    res = client.get("/")
    assert res.status_code == 200
    assert "ComicCraft" in res.text
    assert "Comic Story Creator" in res.text or "Create Your Comic" in res.text
    assert "Classic Comic Book" in res.text

def test_gallery_page():
    """Verify gallery page renders correctly."""
    res = client.get("/gallery")
    assert res.status_code == 200
    assert "Gallery" in res.text

@pytest.mark.asyncio
async def test_story_generation():
    """Verify story generation returns structured comic script."""
    story = await generate_comic_story(
        prompt="A space explorer lands on a neon crystal planet",
        character_name="Captain Nova",
        art_style="Cyberpunk Sci-Fi",
        panel_count=3
    )
    assert "title" in story
    assert "panels" in story
    assert len(story["panels"]) == 3
    for p in story["panels"]:
        assert "panel_title" in p
        assert "dialogue" in p
        assert "image_prompt" in p

@pytest.mark.asyncio
async def test_panel_and_layout_pipeline():
    """Verify panel enrichment and layout positioning calculations."""
    story = await generate_comic_story(
        prompt="Testing clockwork dragon battle",
        character_name="Kael",
        art_style="Manga / Anime",
        panel_count=4
    )
    processed = process_comic_panels(story, "Manga / Anime")
    assert len(processed) == 4
    
    laid_out = calculate_panel_layout(processed)
    assert len(laid_out) == 4
    for p in laid_out:
        assert "grid_span" in p
        assert "bubble_position" in p

@pytest.mark.asyncio
async def test_image_and_pdf_export(tmp_path):
    """Verify image creation and PDF export compile successfully into a valid PDF file."""
    comic_id = "test_comic_123"
    img_url = await generate_panel_image(
        prompt="A valiant hero standing in a storm, comic art",
        comic_id=comic_id,
        panel_number=1,
        panel_title="The Storm",
        sound_effect="CRASH!",
        art_style="Classic Comic Book"
    )
    assert img_url.startswith("/static/outputs/")
    
    # Check that image exists on disk
    img_filename = Path(img_url).name
    img_path = config.OUTPUT_DIR / img_filename
    assert img_path.exists()
    assert img_path.stat().st_size > 0

    comic_data = {
        "id": comic_id,
        "title": "The Storm Chronicles",
        "synopsis": "A hero braves the electrical tempest to save the realm.",
        "genre": "Fantasy",
        "art_style": "Classic Comic Book",
        "character_name": "Valiant",
        "panels": [
            {
                "panel_number": 1,
                "panel_title": "The Storm",
                "caption": "The skies roared with unyielding fury.",
                "dialogue": "Valiant: 'I will not falter!'",
                "speaker": "Valiant",
                "dialogue_text": "I will not falter!",
                "sound_effect": "CRASH!",
                "image_url": img_url,
                "is_hero_panel": True
            }
        ]
    }
    
    pdf_url = export_comic_to_pdf(comic_data)
    assert pdf_url.endswith(".pdf")
    pdf_path = config.OUTPUT_DIR / f"{comic_id}.pdf"
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000  # Non-empty PDF with binary header

def test_api_generate_endpoint():
    """Verify POST /api/generate creates a complete comic."""
    payload = {
        "prompt": "Detective chasing a phantom through rain-slicked alleys",
        "character_name": "Detective Vance",
        "art_style": "Dark Graphic Novel",
        "panel_count": 2
    }
    res = client.post("/api/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert data["title"] is not None
    assert len(data["panels"]) == 2
    assert data["pdf_url"] is not None
