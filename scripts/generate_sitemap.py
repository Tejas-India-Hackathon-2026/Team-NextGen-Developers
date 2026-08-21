import json
import os
from datetime import datetime

def generate_sitemap(meta_path: str = "materials_meta.json", output_dir: str = "docs"):
    """Generate structured JSON and XML sitemap for platform study materials."""
    if not os.path.exists(meta_path):
        print(f"[ERROR] '{meta_path}' not found.")
        return
        
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    
    entries = []
    for filename, data in meta.items():
        if data.get("status") == "Approved":
            entries.append({
                "loc": f"/materials/{filename}",
                "title": data.get("title", filename),
                "subject": data.get("subject", "General"),
                "lastmod": data.get("timestamp", datetime.now().isoformat()[:10]),
                "rating": data.get("rating", 5.0)
            })
            
    # Write JSON sitemap
    json_path = os.path.join(output_dir, "sitemap.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.now().isoformat(), "total": len(entries), "urls": entries}, f, indent=2)
        
    print(f"[SUCCESS] Generated sitemap catalog with {len(entries)} items at {json_path}")

if __name__ == "__main__":
    generate_sitemap()
