import logging
from typing import Dict, Any, List
from app import config

logger = logging.getLogger(__name__)

def get_style_modifier(art_style: str) -> str:
    """Finds matching prompt suffix modifiers for a given art style."""
    for style in config.SUPPORTED_STYLES:
        if style["name"].lower() == art_style.lower() or style["id"] == art_style.lower():
            return style["prompt_suffix"]
    return "classic American comic book illustration, dynamic perspective, sharp inking, vibrant palette"

def process_comic_panels(comic_data: Dict[str, Any], art_style: str) -> List[Dict[str, Any]]:
    """
    Enriches each panel outline with style modifiers, layout aspect ratio flags,
    and formatted dialog segments for the layout and image generator.
    """
    style_modifier = get_style_modifier(art_style)
    processed_panels = []
    
    panels = comic_data.get("panels", [])
    total_panels = len(panels)
    
    for idx, panel in enumerate(panels):
        panel_num = panel.get("panel_number", idx + 1)
        base_prompt = panel.get("image_prompt") or panel.get("visual_description", "")
        
        # Determine panel grid emphasis: first and last panels can be wider/heroic
        is_hero_panel = (idx == 0 or idx == total_panels - 1) and total_panels in (3, 5)
        aspect_ratio = "16:9" if is_hero_panel else "1:1"
        
        # Refined prompt for AI image generator
        full_image_prompt = f"{base_prompt}, {style_modifier}, comic book panel, graphic novel quality, high detail, masterpiece"
        
        # Split character name and dialogue text if present
        raw_dialogue = panel.get("dialogue", "")
        speaker = panel.get("character_name", "")
        dialogue_text = raw_dialogue
        
        if ":" in raw_dialogue:
            parts = raw_dialogue.split(":", 1)
            speaker = parts[0].strip()
            dialogue_text = parts[1].strip().strip('"').strip("'")
            
        processed_panels.append({
            "panel_number": panel_num,
            "panel_title": panel.get("panel_title", f"Panel {panel_num}"),
            "visual_description": panel.get("visual_description", ""),
            "caption": panel.get("caption", ""),
            "dialogue": raw_dialogue,
            "speaker": speaker,
            "dialogue_text": dialogue_text,
            "sound_effect": panel.get("sound_effect", ""),
            "image_prompt": full_image_prompt,
            "aspect_ratio": aspect_ratio,
            "is_hero_panel": is_hero_panel,
            "image_url": panel.get("image_url", "")
        })
        
    return processed_panels
