import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from app import config

logger = logging.getLogger(__name__)
DB_FILE = config.DATA_DIR / "comics.json"

def _load_db() -> Dict[str, Any]:
    if not DB_FILE.exists():
        return {"comics": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {DB_FILE}: {e}")
        return {"comics": []}

def _save_db(data: Dict[str, Any]):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving to {DB_FILE}: {e}")

def save_comic(comic: Dict[str, Any]) -> Dict[str, Any]:
    db = _load_db()
    comic["created_at"] = comic.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if exists
    existing_idx = next((i for i, c in enumerate(db["comics"]) if c.get("id") == comic.get("id")), None)
    if existing_idx is not None:
        db["comics"][existing_idx] = comic
    else:
        db["comics"].insert(0, comic) # Newest first
        
    _save_db(db)
    return comic

def get_comic(comic_id: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    for c in db["comics"]:
        if c.get("id") == comic_id:
            return c
    return None

def list_comics() -> List[Dict[str, Any]]:
    db = _load_db()
    return db.get("comics", [])

def delete_comic(comic_id: str) -> bool:
    db = _load_db()
    initial_len = len(db["comics"])
    db["comics"] = [c for c in db["comics"] if c.get("id") != comic_id]
    if len(db["comics"]) < initial_len:
        _save_db(db)
        return True
    return False

def toggle_comic_favorite(comic_id: str, user_id: str = "guest") -> Dict[str, Any]:
    """Toggles favorite state for a user and updates comic like counter."""
    db = _load_db()
    favs = db.setdefault("favorites", {})
    user_favs = set(favs.get(user_id, []))
    is_fav = comic_id in user_favs
    if is_fav:
        user_favs.remove(comic_id)
        now_fav = False
    else:
        user_favs.add(comic_id)
        now_fav = True
    favs[user_id] = list(user_favs)
    
    # Update like count on the comic object
    likes = 0
    for c in db.get("comics", []):
        if c.get("id") == comic_id:
            c["likes"] = max(0, c.get("likes", 0) + (1 if now_fav else -1))
            likes = c["likes"]
            break
            
    _save_db(db)
    return {"comic_id": comic_id, "is_favorite": now_fav, "likes": likes}

def get_user_favorites(user_id: str = "guest") -> List[str]:
    """Retrieves list of favorite comic IDs for a user."""
    db = _load_db()
    return db.get("favorites", {}).get(user_id, [])

