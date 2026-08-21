from datetime import datetime

def add_material_review(material_meta: dict, username: str, rating: int, comment: str) -> dict:
    """Add or update student star rating and review on a study material."""
    if "reviews" not in material_meta:
        material_meta["reviews"] = []
        
    rating = max(1, min(5, int(rating)))
    
    # Check if user already reviewed
    existing = False
    for r in material_meta["reviews"]:
        if r.get("username") == username:
            r["rating"] = rating
            r["comment"] = comment
            r["updated_at"] = datetime.now().isoformat()
            existing = True
            break
            
    if not existing:
        material_meta["reviews"].append({
            "username": username,
            "rating": rating,
            "comment": comment,
            "upvotes": 0,
            "created_at": datetime.now().isoformat()
        })
        
    # Recalculate average rating
    all_ratings = [r["rating"] for r in material_meta["reviews"]]
    material_meta["rating"] = round(sum(all_ratings) / len(all_ratings), 1)
    material_meta["review_count"] = len(material_meta["reviews"])
    return material_meta

def upvote_review(material_meta: dict, review_index: int) -> bool:
    """Upvote a specific helpful peer review."""
    reviews = material_meta.get("reviews", [])
    if 0 <= review_index < len(reviews):
        reviews[review_index]["upvotes"] = reviews[review_index].get("upvotes", 0) + 1
        return True
    return False
