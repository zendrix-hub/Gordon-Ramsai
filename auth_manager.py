import json
import os
from pathlib import Path

_DB_FILE = Path(__file__).parent / "users.json"

def load_users() -> dict:
    if not _DB_FILE.exists():
        return {}
    try:
        with open(_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(db: dict):
    try:
        with open(_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)
    except Exception as e:
        print(f"Error saving user database: {e}")

def register_user(username, password, profile) -> bool:
    username = username.strip().lower()
    if not username or not password:
        return False
    db = load_users()
    if username in db:
        return False # User already exists
        
    db[username] = {
        "password": password, 
        "profile": profile,
        "tracker": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0},
        "messages": [{
            "role": "assistant",
            "content": f"Listen to me! I'm Gordon RamsAi. Welcome to your kitchen, Chef {username}. We're not doing fads, we're doing the standard. What are we grinding today? LFG!"
        }]
    }
    save_users(db)
    return True

def authenticate_user(username, password) -> bool:
    username = username.strip().lower()
    db = load_users()
    if username not in db:
        return False
    return db[username]["password"] == password

def get_user_data(username) -> dict:
    username = username.strip().lower()
    db = load_users()
    return db.get(username, {})

def save_user_data(username, profile, tracker, messages):
    username = username.strip().lower()
    db = load_users()
    if username in db:
        db[username]["profile"] = profile
        db[username]["tracker"] = tracker
        db[username]["messages"] = messages
        save_users(db)
