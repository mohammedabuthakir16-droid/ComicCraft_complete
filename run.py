import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import config
from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Interactive AI comic book generator powered by Google Gemini Models, dynamic panel layouts, and print-ready PDF export.",
    version="1.0.0"
)

# Mount static folder for CSS, JS, generated images, and PDFs
app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

# Include routes
app.include_router(router)

if __name__ == "__main__":
    print(f"🚀 Starting ComicCraft on http://{config.HOST}:{config.PORT}")
    uvicorn.run(
        "run:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
