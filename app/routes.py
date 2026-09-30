import asyncio
import base64
import json
import logging
import os
import re
import time
import urllib.parse
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app import config
from app.gemini_api import generate_comic_story, enhance_story_prompt
from app.panel_gen import process_comic_panels
from app.image_gen import generate_panel_image
from app.layout import calculate_panel_layout
from app.pdf_export import export_comic_to_pdf
from app.storage import save_comic, get_comic, list_comics, delete_comic

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory=str(config.BASE_DIR / "templates"))
router = APIRouter()

class AuthLoginRequest(BaseModel):
    provider: str = Field("email", description="Authentication provider: 'google', 'apple', 'email', or 'direct'")
    credential: Optional[str] = Field(None, description="OAuth credential or ID token")
    email: Optional[str] = Field(None, description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    password: Optional[str] = Field(None, description="User password (optional for instant sign in)")
    avatar_url: Optional[str] = Field(None, description="User profile photo URL")

def decode_jwt_unverified(token: str) -> Optional[dict]:
    """Decodes JWT payload without signature verification for client ID token parsing."""
    try:
        parts = token.split(".")
        if len(parts) >= 2:
            payload = parts[1]
            padded = payload + "=" * (-len(payload) % 4)
            data = json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))
            return data
    except Exception:
        pass
    return None

def get_current_user_from_request(request: Request) -> Optional[dict]:
    """Retrieves the authenticated user payload from the session cookie."""
    cookie_val = request.cookies.get("comiccraft_user")
    if not cookie_val:
        return None
    try:
        decoded = base64.b64decode(cookie_val.encode("utf-8")).decode("utf-8")
        return json.loads(decoded)
    except Exception:
        return None


class ComicGenerateRequest(BaseModel):
    prompt: str = Field(..., description="Story premise or idea for the comic")
    character_name: Optional[str] = Field("Hero", description="Main character name or persona")
    art_style: Optional[str] = Field("Classic Comic Book", description="Chosen comic art style")
    panel_count: Optional[int] = Field(4, ge=2, le=6, description="Number of panels (2 to 6)")

class PanelRegenerateRequest(BaseModel):
    comic_id: str
    panel_number: int
    prompt_override: Optional[str] = None

class EnhancePromptRequest(BaseModel):
    prompt: str = Field(..., description="Original raw prompt to enhance")
    character_name: Optional[str] = Field("Hero", description="Main character name")
    art_style: Optional[str] = Field("Classic Comic Book", description="Visual style")

class PanelTextUpdateRequest(BaseModel):
    comic_id: str
    panel_number: int
    speaker: Optional[str] = None
    dialogue: Optional[str] = None
    caption: Optional[str] = None
    sound_effect: Optional[str] = None

class ApiKeyUpdateRequest(BaseModel):
    api_key: str = Field(..., description="Google Gemini API key")



@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Renders the ComicCraft home studio dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "styles": config.SUPPORTED_STYLES,
            "genres": config.STORY_GENRES,
            "default_model": config.TEXT_MODEL,
            "has_api_key": bool(config.GEMINI_API_KEY),
            "current_user": get_current_user_from_request(request)
        }
    )

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic_form(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Hero"),
    art_style: str = Form("Classic Comic Book"),
    panel_count: int = Form(4)
):
    """
    Form submission handler:
    1. Uses Gemini to write story & dialogues.
    2. Builds panel prompts.
    3. Generates illustrations for each panel.
    4. Computes responsive comic layout.
    5. Exports PDF.
    6. Saves to database and redirects to result page.
    """
    comic_id = f"comic_{uuid.uuid4().hex[:10]}"
    logger.info(f"Generating new comic [{comic_id}] - '{prompt[:50]}...' with {panel_count} panels in style '{art_style}'")
    
    # Step 1: Gemini story and dialogues
    raw_story = await generate_comic_story(
        prompt=prompt,
        character_name=character_name,
        art_style=art_style,
        panel_count=panel_count
    )
    
    # Step 2: Process panel metadata and styles
    processed_panels = process_comic_panels(raw_story, art_style)
    
    # Step 3: Generate images for each panel with polite staggering
    for idx, panel in enumerate(processed_panels):
        img_url = await generate_panel_image(
            prompt=panel["image_prompt"],
            comic_id=comic_id,
            panel_number=panel["panel_number"],
            panel_title=panel["panel_title"],
            sound_effect=panel.get("sound_effect", ""),
            art_style=art_style
        )
        panel["image_url"] = img_url
        if idx < len(processed_panels) - 1:
            await asyncio.sleep(0.6)
        
    # Step 4: Layout calculations
    final_panels = calculate_panel_layout(processed_panels)
    
    comic_data = {
        "id": comic_id,
        "title": raw_story.get("title", "A Comic Tale"),
        "synopsis": raw_story.get("synopsis", prompt),
        "genre": raw_story.get("genre", "Action & Adventure"),
        "art_style": art_style,
        "character_name": character_name,
        "prompt": prompt,
        "panel_count": len(final_panels),
        "panels": final_panels
    }
    
    # Step 5: Export to PDF
    pdf_url = export_comic_to_pdf(comic_data)
    comic_data["pdf_url"] = pdf_url
    
    # Step 6: Save
    save_comic(comic_data)
    
    return RedirectResponse(url=f"/comic/{comic_id}", status_code=303)

@router.get("/comic/{comic_id}", response_class=HTMLResponse)
async def view_comic(request: Request, comic_id: str):
    """Renders the Comic Result / Preview page."""
    comic = get_comic(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
        
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "comic": comic,
            "styles": config.SUPPORTED_STYLES,
            "current_user": get_current_user_from_request(request)
        }
    )

@router.get("/download/{comic_id}")
async def download_comic_pdf(comic_id: str):
    """Direct PDF download endpoint."""
    comic = get_comic(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
        
    pdf_path = config.OUTPUT_DIR / f"{comic_id}.pdf"
    if not pdf_path.exists():
        # Re-export if missing
        export_comic_to_pdf(comic)
        
    if not pdf_path.exists():
        raise HTTPException(status_code=500, detail="Could not generate PDF")
        
    safe_filename = f"{comic.get('title', 'comic')[:30].replace(' ', '_')}.pdf"
    return FileResponse(
        path=str(pdf_path),
        filename=safe_filename,
        media_type="application/pdf"
    )

@router.get("/success/{comic_id}", response_class=HTMLResponse)
async def comic_export_success_page(request: Request, comic_id: str):
    """
    Renders the Comic Export Success Page shown in the SmartInternz project specification,
    confirming export and offering next actions.
    """
    comic = get_comic(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
        
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "comic": comic,
            "current_user": get_current_user_from_request(request)
        }
    )

@router.get("/gallery", response_class=HTMLResponse)
async def comic_gallery(request: Request):
    """Shows all previously created comics in a visual showcase gallery."""
    all_comics = list_comics()
    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={
            "comics": all_comics,
            "current_user": get_current_user_from_request(request)
        }
    )

@router.post("/delete/{comic_id}")
async def delete_comic_route(comic_id: str):
    """Deletes a comic entry."""
    delete_comic(comic_id)
    return RedirectResponse(url="/gallery", status_code=303)

# ----------------- REST API Endpoints ----------------- #

@router.post("/api/generate")
async def api_generate_comic(payload: ComicGenerateRequest):
    """REST API endpoint to generate comic programmatically."""
    comic_id = f"comic_{uuid.uuid4().hex[:10]}"
    raw_story = await generate_comic_story(
        prompt=payload.prompt,
        character_name=payload.character_name or "Hero",
        art_style=payload.art_style or "Classic Comic Book",
        panel_count=payload.panel_count or 4
    )
    processed_panels = process_comic_panels(raw_story, payload.art_style or "Classic Comic Book")
    for panel in processed_panels:
        img_url = await generate_panel_image(
            prompt=panel["image_prompt"],
            comic_id=comic_id,
            panel_number=panel["panel_number"],
            panel_title=panel["panel_title"],
            sound_effect=panel.get("sound_effect", ""),
            art_style=payload.art_style or "Classic Comic Book"
        )
        panel["image_url"] = img_url
        
    final_panels = calculate_panel_layout(processed_panels)
    comic_data = {
        "id": comic_id,
        "title": raw_story.get("title", "A Comic Tale"),
        "synopsis": raw_story.get("synopsis", payload.prompt),
        "genre": raw_story.get("genre", "Action & Adventure"),
        "art_style": payload.art_style,
        "character_name": payload.character_name,
        "prompt": payload.prompt,
        "panel_count": len(final_panels),
        "panels": final_panels
    }
    pdf_url = export_comic_to_pdf(comic_data)
    comic_data["pdf_url"] = pdf_url
    save_comic(comic_data)
    return comic_data

@router.post("/api/regenerate-panel")
async def api_regenerate_panel(payload: PanelRegenerateRequest):
    """Regenerates a single panel image and re-exports the comic PDF."""
    comic = get_comic(payload.comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")

    target_panel = None
    for p in comic.get("panels", []):
        if p.get("panel_number") == payload.panel_number:
            target_panel = p
            break

    if not target_panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    prompt_to_use = payload.prompt_override or target_panel.get("image_prompt", "")
    new_img_url = await generate_panel_image(
        prompt=prompt_to_use,
        comic_id=payload.comic_id,
        panel_number=payload.panel_number,
        panel_title=target_panel.get("panel_title", "Panel"),
        sound_effect=target_panel.get("sound_effect", ""),
        art_style=comic.get("art_style", "Classic Comic Book"),
        force_regenerate=True
    )

    target_panel["image_url"] = new_img_url
    
    # Re-export PDF with the new image
    try:
        export_comic_to_pdf(comic)
    except Exception as e:
        logger.warning(f"PDF re-export failed during panel regeneration: {e}")

    save_comic(comic)
    return {
        "status": "success",
        "comic_id": payload.comic_id,
        "panel_number": payload.panel_number,
        "image_url": new_img_url
    }

@router.post("/api/enhance-prompt")
async def api_enhance_prompt(payload: EnhancePromptRequest):
    """Enriches and expands a brief prompt into a vivid, cinematic comic premise."""
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    enhanced = await enhance_story_prompt(
        prompt=payload.prompt,
        character_name=payload.character_name or "Hero",
        art_style=payload.art_style or "Classic Comic Book"
    )
    return {
        "status": "success",
        "original": payload.prompt,
        "enhanced_prompt": enhanced
    }

@router.post("/api/update-panel-text")
async def api_update_panel_text(payload: PanelTextUpdateRequest):
    """Updates dialogue, speaker, caption, or sound effect for a specific panel and refreshes the PDF."""
    comic = get_comic(payload.comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")

    target_panel = None
    for p in comic.get("panels", []):
        if p.get("panel_number") == payload.panel_number:
            target_panel = p
            break

    if not target_panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    if payload.speaker is not None:
        target_panel["speaker"] = payload.speaker.strip()
    if payload.dialogue is not None:
        target_panel["dialogue_text"] = payload.dialogue.strip()
        speaker = target_panel.get("speaker", "Character")
        target_panel["dialogue"] = f"{speaker}: '{payload.dialogue.strip()}'"
    if payload.caption is not None:
        target_panel["caption"] = payload.caption.strip()
    if payload.sound_effect is not None:
        target_panel["sound_effect"] = payload.sound_effect.strip().upper()

    # Re-export PDF with the new text
    try:
        export_comic_to_pdf(comic)
    except Exception as e:
        logger.warning(f"PDF re-export failed during panel text update: {e}")

    save_comic(comic)
    return {
        "status": "success",
        "comic_id": payload.comic_id,
        "panel_number": payload.panel_number,
        "panel": target_panel
    }

@router.post("/api/settings/gemini-key")
async def update_gemini_api_key(payload: ApiKeyUpdateRequest):
    """Validates the Gemini API key and updates server config and .env file."""
    candidate_key = payload.api_key.strip()
    if not candidate_key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")

    # Validate against Gemini API
    verification_passed = False
    error_msg = ""

    try:
        from google import genai
        client = genai.Client(api_key=candidate_key)
        test_res = client.models.generate_content(
            model=config.TEXT_MODEL,
            contents=["Respond with only the word 'VALID'"]
        )
        if test_res and test_res.text:
            verification_passed = True
    except Exception as e:
        error_msg = str(e)
        logger.warning(f"google.genai verification failed: {e}. Trying fallback client...")

    if not verification_passed:
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=candidate_key)
            model = genai_legacy.GenerativeModel("gemini-1.5-flash")
            test_res = model.generate_content("Respond with only the word 'VALID'")
            if test_res and test_res.text:
                verification_passed = True
        except Exception as e2:
            error_msg = f"{error_msg}; {str(e2)}"
            logger.warning(f"Legacy Gemini verification failed: {e2}")

    if not verification_passed:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Verification failed. Please check your Gemini API key: {error_msg}"
            }
        )

    # Key is verified! Update runtime configuration
    config.GEMINI_API_KEY = candidate_key
    os.environ["GEMINI_API_KEY"] = candidate_key

    # Persist into .env file safely
    env_path = config.BASE_DIR / ".env"
    try:
        content = ""
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")
        if re.search(r"^GEMINI_API_KEY=.*", content, flags=re.MULTILINE):
            new_content = re.sub(r"^GEMINI_API_KEY=.*", f"GEMINI_API_KEY={candidate_key}", content, flags=re.MULTILINE)
        else:
            new_content = content.strip() + f"\nGEMINI_API_KEY={candidate_key}\n"
        env_path.write_text(new_content, encoding="utf-8")
    except Exception as err:
        logger.warning(f"Could not persist GEMINI_API_KEY to .env: {err}")

    return {
        "status": "success",
        "message": "Google Gemini 2.5 Flash API Key verified and activated successfully!",
        "model": config.TEXT_MODEL,
        "masked_key": candidate_key[:6] + "..." + candidate_key[-4:]
    }

@router.get("/api/settings/status")
async def get_settings_status():
    """Returns whether Gemini API is active, masking the key."""
    has_key = bool(config.GEMINI_API_KEY)
    masked_key = ""
    if has_key:
        masked_key = config.GEMINI_API_KEY[:6] + "..." + config.GEMINI_API_KEY[-4:]
    return {
        "gemini_api_configured": has_key,
        "masked_key": masked_key,
        "model": config.TEXT_MODEL,
        "image_provider": config.IMAGE_PROVIDER
    }

# ----------------- Authentication Endpoints (Google & Apple) ----------------- #

@router.post("/api/auth/login")
async def api_auth_login(payload: AuthLoginRequest):
    """
    Authenticates a user via Direct Email/Name Sign-In, Google Sign-In, or Apple Sign-In.
    Supports user's own identity, real OAuth credential tokens, or instant verification.
    """
    provider = (payload.provider or "email").lower().strip()
    if provider not in ("google", "apple", "email", "direct"):
        raise HTTPException(status_code=400, detail="Unsupported auth provider. Use 'google', 'apple', or 'email'.")

    raw_name = (payload.name or "").strip()
    raw_email = (payload.email or "").strip()
    avatar_url = payload.avatar_url

    # If real credential token is passed (e.g. from Google Identity Services)
    if payload.credential:
        token_data = decode_jwt_unverified(payload.credential)
        if token_data:
            raw_name = raw_name or token_data.get("name") or token_data.get("given_name", "")
            raw_email = raw_email or token_data.get("email", "")
            avatar_url = avatar_url or token_data.get("picture", "")

    # Provider and identity resolution
    if provider == "google":
        provider_title = "Google"
        provider_id = "google"
        user_name = raw_name or (raw_email.split("@")[0].capitalize() if raw_email else "Alex Rivera")
        user_email = raw_email or (f"{user_name.lower().replace(' ', '.')}@gmail.com" if raw_name else "alex.rivera@gmail.com")
        if not avatar_url:
            encoded_name = urllib.parse.quote(user_name)
            avatar_url = f"https://ui-avatars.com/api/?name={encoded_name}&background=4285F4&color=fff&bold=true&rounded=true"
    elif provider == "apple":
        provider_title = "Apple"
        provider_id = "apple"
        user_name = raw_name or (raw_email.split("@")[0].capitalize() if raw_email else "Jordan Vance")
        user_email = raw_email or (f"{user_name.lower().replace(' ', '.')}@privaterelay.appleid.com" if raw_name else "jordan.vance@privaterelay.appleid.com")
        if not avatar_url:
            encoded_name = urllib.parse.quote(user_name)
            avatar_url = f"https://ui-avatars.com/api/?name={encoded_name}&background=000000&color=fff&bold=true&rounded=true"
    else:  # email or direct
        provider_title = "ComicCraft ID"
        provider_id = "email"
        user_name = raw_name or (raw_email.split("@")[0].capitalize() if raw_email else "Comic Creator")
        user_email = raw_email or "creator@comiccraft.ai"
        if not avatar_url:
            encoded_name = urllib.parse.quote(user_name)
            avatar_url = f"https://ui-avatars.com/api/?name={encoded_name}&background=2563eb&color=fff&bold=true&rounded=true"

    user = {
        "id": f"usr_{uuid.uuid4().hex[:8]}",
        "name": user_name,
        "email": user_email,
        "avatar_url": avatar_url,
        "provider": provider_title,
        "provider_id": provider_id,
        "logged_in_at": time.time()
    }

    encoded = base64.b64encode(json.dumps(user).encode("utf-8")).decode("utf-8")
    response = JSONResponse(
        content={
            "status": "success",
            "message": f"Successfully signed in as {user_name}!",
            "user": user
        }
    )
    response.set_cookie(
        key="comiccraft_user",
        value=encoded,
        max_age=30 * 86400,
        httponly=False,
        samesite="lax"
    )
    return response

@router.get("/api/auth/me")
async def api_auth_me(request: Request):
    """Returns the currently authenticated user profile and session state."""
    user = get_current_user_from_request(request)
    if user:
        return {"authenticated": True, "user": user}
    return {"authenticated": False, "user": None}

@router.post("/api/auth/logout")
async def api_auth_logout():
    """Logs the user out and clears the authentication cookie."""
    response = JSONResponse(
        content={
            "status": "success",
            "message": "Signed out successfully"
        }
    )
    response.delete_cookie(key="comiccraft_user")
    return response

@router.get("/health")
async def health_check():
    """Health status and configuration inspection."""
    return {
        "status": "healthy",
        "app": "ComicCraft - AI Comic Story Creator",
        "gemini_api_configured": bool(config.GEMINI_API_KEY),
        "text_model": config.TEXT_MODEL,
        "image_provider": config.IMAGE_PROVIDER
    }
