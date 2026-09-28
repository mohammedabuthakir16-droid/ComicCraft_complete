# 💥 ComicCraft — AI Comic Story Creator using Gemini Models

An end-to-end AI Comic Book Studio and Storyboard Creator powered by **Google Gemini Models**, **FastAPI**, dynamic comic book layouts, and **FPDF** print-ready PDF export.

Based on the **Skill Wallet / SmartInternz AI & Cloud Engineering Project** featured in the video walkthrough: *"ComicCraft - AI Comic Story Creator using Gemini Models"*.

---

## 🌟 Overview & Key Features

- **🧠 Gemini Narrative Engine**: Crafts coherent multi-panel comic scripts, plot arcs, dynamic scene directions, character dialogue, and action sound effects (`gemini-2.5-flash` / `gemini-1.5-flash`).
- **🎨 Multi-Style Art Synthesis**: Generates panel illustrations matching chosen comic styles (Classic American Comic, Japanese Manga, Dark Noir Graphic Novel, Cyberpunk, Indie Watercolor, and Pop Art).
- **💬 Dynamic Comic Layout**: Renders authentic comic book grids with dialogue balloons, speech pointers, narration caption boxes, and onomatopoeia badges (POW!, WHAM!, KABOOM!).
- **📄 One-Click PDF Comic Book Export**: Compiles all panels into a downloadable, print-ready, high-resolution A4 PDF comic book.
- **📚 Comic Gallery & Archive**: Automatically saves created comics to revisit, read, and re-export.
- **⚡ Zero-Config Fallback & Production-Ready**: Works out of the box with zero external dependencies via offline creative engine, or connects seamlessly to live Gemini and Image APIs.

---

## 🏗️ Architecture & Workflow

```
+-------------------------------------------------------------+
|                      USER INTERFACE                         |
|  - Story Premise Input                                      |
|  - Character Persona & Art Style Selector (Manga, Noir,...) |
|  - Panel Count (3 to 6 Panels)                              |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               FASTAPI BACKEND (run.py / routes.py)          |
+------------------------------+------------------------------+
                               |
         +---------------------+---------------------+
         |                                           |
         v                                           v
+-----------------------------+             +-----------------------------+
|     GEMINI AI ENGINE        |             |      PANEL PROCESSOR        |
|  - Story & Arc Scripting    |             |  - Prompt Enhancement       |
|  - Character Dialogues      |             |  - Style Modifiers          |
|  - Onomatopoeia Selection   |             |  - Grid Span Calculations   |
+--------------+--------------+             +--------------+--------------+
               |                                           |
               +---------------------+---------------------+
                                     |
                                     v
+-------------------------------------------------------------+
|                    IMAGE GENERATOR ENGINE                   |
|  - Pollinations AI / HuggingFace Stable Diffusion           |
|  - Procedural Comic Illustrator Fallback                    |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                      LAYOUT & RENDERING                     |
|  - Responsive HTML5/CSS3 Comic Book Grid                    |
|  - Speech Bubble Tails & Dialogue Anchoring                 |
|  - Ben-Day Halftone Dot & Action Starburst Badges           |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     PDF COMPILER (FPDF2)                    |
|  - Multi-page Comic Strip Book                              |
|  - Formatted Narrations, Issue Numbers & Banner             |
|  - Direct Download & Export Confirmation Page               |
+-------------------------------------------------------------+
```

---

## 📁 Project Structure

```
comiccraft/
├── app/
│   ├── __init__.py           # App initialization
│   ├── config.py             # Environment configuration & style definitions
│   ├── gemini_api.py         # Google Gemini LLM story & dialogue generator
│   ├── panel_gen.py          # Panel structuring & prompt enrichment
│   ├── image_gen.py          # AI & procedural comic illustration generator
│   ├── layout.py             # Comic grid layout & speech bubble positions
│   ├── pdf_export.py         # FPDF comic book compiler
│   ├── storage.py            # Local JSON database & comic persistence
│   └── routes.py             # Web routes & REST API endpoints
├── templates/
│   ├── base.html             # Base layout with comic navigation & theme
│   ├── index.html            # Studio dashboard & comic creation form
│   ├── result.html           # Comic viewer with speech bubbles & action bar
│   ├── gallery.html          # Comic shelf archive of past creations
│   └── success.html          # Export confirmation page
├── static/
│   ├── css/
│   │   └── styles.css        # Comic book typography, halftone dots, borders
│   ├── js/
│   │   └── main.js           # Loading animations & interactive behaviors
│   ├── images/               # Static icons & stickers
│   └── outputs/              # Generated panel images and exported PDFs
├── data/
│   └── comics.json           # Comic stories database
├── tests/
│   └── test_app.py           # Pytest automated test suite
├── run.py                    # Application entrypoint
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Local configuration
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (or [uv](https://astral.sh/uv))
- A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/) *(optional for basic offline demo)*

### 2. Setup Virtual Environment & Install Dependencies

Using `uv` (recommended, ultra-fast):
```bash
cd comiccraft
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or using standard `pip`:
```bash
cd comiccraft
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and add your Gemini API Key:
```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
TEXT_MODEL=gemini-2.5-flash
IMAGE_PROVIDER=pollinations
PORT=8000
```

### 4. Run the Application
```bash
python run.py
```
Open your browser and navigate to:
👉 **`http://localhost:8000`**

---

## 🧪 Running Automated Tests
Run the test suite with pytest:
```bash
pytest tests/ -v
```

---

## 📡 REST API Documentation

FastAPI provides interactive Swagger documentation out of the box at:
👉 **`http://localhost:8000/docs`**

### Key Endpoints:
- `GET /` — Studio Home Dashboard
- `POST /generate` — Form endpoint to create comic and redirect to result
- `GET /comic/{comic_id}` — View generated comic strip
- `GET /download/{comic_id}` — Download print-ready PDF comic book
- `GET /success/{comic_id}` — Comic export success page
- `GET /gallery` — View all created comics
- `POST /api/generate` — Programmatic JSON API to generate comics
- `GET /health` — Service health check & config status

---

## 🎓 Milestone Breakdown (SmartInternz Curriculum)

1. **Milestone 1: Model Selection & Architecture**
   - Researched and integrated Google Gemini models (`gemini-2.5-flash` / `gemini-1.5-flash`).
   - Designed layered architecture (FastAPI Backend, Gemini Engine, Image Synthesis, Jinja2 Frontend, FPDF Export).
2. **Milestone 2: Core Functionalities Development**
   - Engineered prompts for story arc, character dialogue, and sound effects (`app/gemini_api.py`).
   - Implemented panel processing and aspect-ratio styling (`app/panel_gen.py`).
   - Built multi-provider image generation with offline procedural fallback (`app/image_gen.py`).
   - Developed dynamic layout positioning engine (`app/layout.py`).
   - Created multi-page A4 PDF compiler with speech bubble transcripts (`app/pdf_export.py`).
3. **Milestone 3: Routes Development**
   - Structured complete routing in `app/routes.py` with form handling, error states, and REST APIs.
4. **Milestone 4: Frontend Development**
   - Designed responsive comic book UI in `static/css/styles.css` with halftone dots, comic fonts, and speech balloons.
   - Built dynamic Jinja2 templates (`index.html`, `result.html`, `gallery.html`, `success.html`).
5. **Milestone 5: Testing & Deployment**
   - Wrote comprehensive unit and integration tests (`tests/test_app.py`).
   - Validated end-to-end generation, local serving, and PDF downloads.
