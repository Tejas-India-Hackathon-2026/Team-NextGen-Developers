import json
import os
import uuid
from datetime import datetime

NOTIFICATIONS_FILE = "data/notifications.json"

def send_notification(recipient: str, title: str, message: str, category: str = "general", db_path: str = NOTIFICATIONS_FILE) -> dict:
    """Create and store a targeted notification."""
    notif = {
        "id": str(uuid.uuid4())[:8],
        "recipient": recipient,
        "title": title,
        "message": message,
        "category": category,
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    all_notifs = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                all_notifs = json.load(f)
                if not isinstance(all_notifs, list):
                    all_notifs = []
        except Exception:
            all_notifs = []
            
    all_notifs.append(notif)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(all_notifs, f, indent=2)
        
    return notif

def get_user_notifications(username: str, unread_only: bool = False, db_path: str = NOTIFICATIONS_FILE) -> list:
    """Get all notifications for a user or broadcast notifications."""
    if not os.path.exists(db_path):
        return []
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            all_notifs = json.load(f)
            if not isinstance(all_notifs, list):
                return []
    except Exception:
        return []
        
    user_notifs = [n for n in all_notifs if n.get("recipient") in (username, "all", "*")]
    if unread_only:
        user_notifs = [n for n in user_notifs if not n.get("read", False)]
    return sorted(user_notifs, key=lambda x: x.get("timestamp", ""), reverse=True)

def mark_as_read(notif_id: str, db_path: str = NOTIFICATIONS_FILE) -> bool:
    """Mark a notification as read."""
    if not os.path.exists(db_path):
        return False
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            all_notifs = json.load(f)
        found = False
        for n in all_notifs:
            if n.get("id") == notif_id:
                n["read"] = True
                found = True
                break
        if found:
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(all_notifs, f, indent=2)
        return found
    except Exception:
        return False
