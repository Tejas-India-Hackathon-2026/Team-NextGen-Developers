"""Personalized study material recommendation engine for students."""

def recommend_materials(user_profile: dict, all_materials: list, user_history: list = None, limit: int = 5) -> list:
    """Recommend study materials based on branch, semester, popularity, and rating."""
    if not all_materials:
        return []
        
    branch = user_profile.get("branch", "")
    semester = user_profile.get("semester", 1)
    viewed_ids = set(user_history or [])
    
    scored_materials = []
    for mat in all_materials:
        mat_id = mat.get("id") or mat.get("title")
        if mat_id in viewed_ids:
            continue
            
        score = 0.0
        # Branch match
        mat_branch = mat.get("branch", "")
        if mat_branch == branch:
            score += 40.0
        elif mat_branch in ("All", "Common", "General"):
            score += 20.0
            
        # Semester match
        mat_sem = mat.get("semester")
        if mat_sem == semester:
            score += 30.0
        elif mat_sem in ("All", "Common"):
            score += 15.0
            
        # Rating boost (up to 15 points)
        rating = float(mat.get("rating", 4.0))
        score += (rating / 5.0) * 15.0
        
        # Download popularity boost (up to 15 points)
        downloads = int(mat.get("downloads", 0))
        score += min(15.0, downloads * 0.5)
        
        scored_materials.append((score, mat))
        
    # Sort by recommendation score descending
    scored_materials.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored_materials[:limit]]
