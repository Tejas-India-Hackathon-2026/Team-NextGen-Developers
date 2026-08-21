import json
import os
import sys
from datetime import datetime

def sync_unregistered_materials(materials_dir: str = "materials", meta_path: str = "materials_meta.json"):
    """Scan materials directory and register any untracked PDF files into metadata store."""
    if not os.path.exists(materials_dir):
        print(f"[ERROR] Materials directory '{materials_dir}' not found.")
        return
        
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception as e:
            print(f"[WARN] Error reading metadata: {e}")
            meta = {}
            
    pdf_files = [f for f in os.listdir(materials_dir) if f.lower().endswith(".pdf")]
    added_count = 0
    
    for filename in pdf_files:
        if filename not in meta:
            title = filename.replace(".pdf", "").replace("_", " ")
            meta[filename] = {
                "title": title,
                "subject": "General Engineering",
                "topic": "Academic Notes",
                "uploaded_by": "system_importer",
                "status": "Approved",
                "rating": 5.0,
                "downloads": 0,
                "timestamp": datetime.now().isoformat(),
                "moderated_by": "admin"
            }
            added_count += 1
            print(f"[ADDED] Registered metadata for: {filename}")
            
    if added_count > 0:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        print(f"[SUCCESS] Registered {added_count} new materials in metadata.")
    else:
        print("[INFO] All PDF materials are already tracked in metadata.")

if __name__ == "__main__":
    sync_unregistered_materials()
