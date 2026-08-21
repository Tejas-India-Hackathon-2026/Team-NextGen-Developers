import json
import os
from datetime import datetime

LOG_FILE = "data/audit_logs.json"

def log_event(event_type: str, actor: str, details: dict, status: str = "SUCCESS", log_path: str = LOG_FILE) -> dict:
    """Log an audit event with timestamp and details."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "actor": actor,
        "status": status,
        "details": details
    }
    
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
        except Exception:
            logs = []
            
    logs.append(entry)
    # Keep last 500 logs to prevent unbounded file growth
    if len(logs) > 500:
        logs = logs[-500:]
        
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
        
    return entry

def query_logs(event_type: str = None, actor: str = None, limit: int = 50, log_path: str = LOG_FILE) -> list:
    """Query and filter audit logs."""
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
            if not isinstance(logs, list):
                return []
    except Exception:
        return []
        
    filtered = logs
    if event_type:
        filtered = [l for l in filtered if l.get("event_type") == event_type]
    if actor:
        filtered = [l for l in filtered if l.get("actor") == actor]
        
    return filtered[-limit:]
