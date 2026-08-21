import os, json, tempfile

def load_json_safe(path: str, default_data=None):
    if not os.path.exists(path): return default_data if default_data is not None else {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_data if default_data is not None else {}
