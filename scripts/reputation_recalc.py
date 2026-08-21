import json
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.gamification import evaluate_badges

def reconcile_user_reputations(users_path: str = "users.json", meta_path: str = "materials_meta.json"):
    """Reconcile user karma points and evaluate badges based on uploaded materials count and ratings."""
    if not os.path.exists(users_path) or not os.path.exists(meta_path):
        print("[ERROR] Users or materials metadata file missing.")
        return
        
    with open(users_path, "r", encoding="utf-8") as f:
        users = json.load(f)
        
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    # Count approved uploads and average ratings per user
    user_stats = {}
    for filename, item in meta.items():
        uploader = item.get("uploaded_by")
        if not uploader:
            continue
        if uploader not in user_stats:
            user_stats[uploader] = {"count": 0, "ratings": []}
        if item.get("status") == "Approved":
            user_stats[uploader]["count"] += 1
            if "rating" in item:
                user_stats[uploader]["ratings"].append(float(item["rating"]))
                
    updates = 0
    for uname, udata in users.items():
        stats = user_stats.get(uname, {"count": 0, "ratings": []})
        upload_count = stats["count"]
        avg_rating = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0.0
        
        # Calculate badges
        earned_badges = evaluate_badges(udata, upload_count, avg_rating)
        if udata.get("badges") != earned_badges:
            udata["badges"] = earned_badges
            updates += 1
            print(f"[UPDATED] Recalculated badges for {uname}: {earned_badges}")
            
    if updates > 0:
        with open(users_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        print(f"[SUCCESS] Reconciled reputation and badges for {updates} users.")
    else:
        print("[INFO] All user badges and karma points are consistent.")

if __name__ == "__main__":
    reconcile_user_reputations()
