"""
ComicCraft - AI Comic Book Generator
Root entry point for VS Code execution and production server.
"""
import uvicorn
from run import app
from app import config

if __name__ == "__main__":
    print(f"🚀 Starting ComicCraft Studio on http://{config.HOST}:{config.PORT}")
    uvicorn.run(
        "run:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
