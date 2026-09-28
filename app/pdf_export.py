import logging
from pathlib import Path
from typing import Dict, Any, List
from fpdf import FPDF
from app import config

logger = logging.getLogger(__name__)

class ComicPDF(FPDF):
    def __init__(self, comic_title: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.comic_title = comic_title
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Comic Header Banner
        self.set_fill_color(24, 24, 27) # Dark comic banner
        self.rect(0, 0, 210, 24, "F")
        
        # Yellow accent line
        self.set_fill_color(250, 204, 21) # Vibrant yellow
        self.rect(0, 24, 210, 2, "F")
        
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 6)
        clean_title = self.comic_title.encode("latin-1", "replace").decode("latin-1")
        self.cell(0, 10, f"COMICCRAFT: {clean_title.upper()}", border=0, align="L")
        
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(250, 204, 21)
        self.set_xy(150, 6)
        self.cell(50, 10, "ISSUE #1 - SPECIAL", border=0, align="R")
        self.ln(20)
        
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | Created with ComicCraft AI & Gemini Models", border=0, align="C")

def clean_pdf_text(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "—": "--",
        "–": "-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "…": "...",
        "•": "*",
        "★": "*",
        "⚡": "*",
        "💥": "!",
        "🦊": "",
        "⚔️": "",
        "🌆": "",
        "🕵️": ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")

def export_comic_to_pdf(comic: Dict[str, Any]) -> str:
    """
    Renders the comic strip into an elegant multi-panel A4 PDF book.
    Returns the web URL path for the generated PDF.
    """
    comic_id = comic.get("id", "comic")
    title = clean_pdf_text(comic.get("title", "ComicCraft Adventure"))
    pdf_filename = f"{comic_id}.pdf"
    pdf_path = config.OUTPUT_DIR / pdf_filename
    
    pdf = ComicPDF(comic_title=title)
    pdf.add_page()
    
    # Comic Cover / Synopsis Intro
    pdf.set_fill_color(254, 240, 138) # Light yellow caption note
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.6)
    pdf.rect(10, 30, 190, 18, "FD")
    
    pdf.set_xy(14, 32)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(180, 83, 9)
    style_text = clean_pdf_text(comic.get('art_style', 'Classic')).upper()
    genre_text = clean_pdf_text(comic.get('genre', 'Adventure')).upper()
    pdf.cell(0, 5, f"STYLE: {style_text} | GENRE: {genre_text}", border=0, new_x="LMARGIN", new_y="NEXT")
    
    synopsis = clean_pdf_text(comic.get("synopsis", ""))
    pdf.set_xy(14, 37)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(182, 4.5, synopsis[:180])
    
    pdf.ln(6)
    
    panels = comic.get("panels", [])
    
    # 2 panels per page
    # Calculate dimensions
    img_w = 95
    img_h = 70
    
    current_y = 54
    for idx, panel in enumerate(panels):
        # If running out of room on the page (need ~95mm per panel pair)
        if current_y > 210:
            pdf.add_page()
            current_y = 32
            
        panel_num = panel.get("panel_number", idx + 1)
        panel_title = clean_pdf_text(panel.get("panel_title", f"Panel {panel_num}"))
        
        # Panel Title Box
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(10, current_y, 190, 7, "F")
        pdf.set_xy(12, current_y + 1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        sound = clean_pdf_text(panel.get("sound_effect", ""))
        clean_sound = f" [{sound}]" if sound else ""
        pdf.cell(186, 5, f"PANEL {panel_num}: {panel_title.upper()}{clean_sound}", border=0, new_x="LMARGIN", new_y="NEXT")
        
        current_y += 8
        
        # Draw Panel Image on the left
        panel_img_url = panel.get("image_url", "")
        # Resolve to local filesystem path
        local_img_path = None
        if panel_img_url:
            filename = Path(panel_img_url).name
            possible_path = config.OUTPUT_DIR / filename
            if possible_path.exists():
                local_img_path = str(possible_path)
                
        # If no image found, fallback to placeholder image
        if local_img_path and Path(local_img_path).exists():
            pdf.image(local_img_path, x=10, y=current_y, w=img_w, h=img_h)
        else:
            # Draw empty placeholder box
            pdf.set_fill_color(240, 240, 240)
            pdf.rect(10, current_y, img_w, img_h, "FD")
            pdf.set_xy(25, current_y + 30)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(120, 120, 120)
            pdf.cell(60, 10, f"[Panel {panel_num} Illustration]", border=0, align="C")
            
        # Draw comic border around image
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.8)
        pdf.rect(10, current_y, img_w, img_h)
        
        # Right Column: Narration Caption & Dialogue Speech Bubble
        text_x = 110
        text_w = 90
        
        # 1. Narration Caption (Yellow box)
        caption = clean_pdf_text(panel.get("caption", ""))
        if caption:
            pdf.set_fill_color(254, 243, 199) # Pale yellow
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.4)
            pdf.rect(text_x, current_y, text_w, 24, "FD")
            
            pdf.set_xy(text_x + 2, current_y + 1)
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(180, 83, 9)
            pdf.cell(text_w - 4, 4, "NARRATION:", border=0, new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_xy(text_x + 2, current_y + 6)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(text_w - 4, 3.8, caption[:160])
            
        # 2. Character Speech Bubble (Rounded white box)
        dialogue = clean_pdf_text(panel.get("dialogue", ""))
        if dialogue:
            dialogue_y = current_y + 28
            pdf.set_fill_color(255, 255, 255)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.6)
            pdf.rect(text_x, dialogue_y, text_w, 36, "FD")
            
            # Speaker header
            speaker = clean_pdf_text(panel.get("speaker", "Character"))
            pdf.set_xy(text_x + 3, dialogue_y + 2)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(225, 29, 72) # Red speaker name
            pdf.cell(text_w - 6, 4, f"{speaker.upper()}:", border=0, new_x="LMARGIN", new_y="NEXT")
            
            # Dialogue quote
            pdf.set_xy(text_x + 3, dialogue_y + 7)
            pdf.set_font("Helvetica", "", 8.5)
            pdf.set_text_color(10, 10, 10)
            clean_text = clean_pdf_text(panel.get("dialogue_text", dialogue))
            pdf.multi_cell(text_w - 6, 4.2, f'"{clean_text[:180]}"')
            
        current_y += img_h + 8
        
    pdf.output(str(pdf_path))
    logger.info(f"Exported comic PDF to {pdf_path}")
    return f"/static/outputs/{pdf_filename}"
