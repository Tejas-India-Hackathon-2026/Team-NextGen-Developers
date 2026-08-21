"""Gamification engine for student karma, badges, and leaderboard calculations."""

BADGE_DEFINITIONS = {
    "FIRST_UPLOAD": {"name": "First Contributor", "icon": "🌱", "desc": "Uploaded first study resource", "min_uploads": 1},
    "PROLIFIC_AUTHOR": {"name": "Prolific Scholar", "icon": "📚", "desc": "Uploaded 5+ verified study materials", "min_uploads": 5},
    "COMMUNITY_PILLAR": {"name": "Community Pillar", "icon": "🏛️", "desc": "Uploaded 10+ verified study materials", "min_uploads": 10},
    "TOP_RATED": {"name": "Master Educator", "icon": "⭐", "desc": "Achieved average rating >= 4.5", "min_rating": 4.5},
    "KARMA_CENTURION": {"name": "Karma Centurion", "icon": "💯", "desc": "Earned 100+ academic karma", "min_karma": 100},
    "CAMPUS_LEGEND": {"name": "Campus Legend", "icon": "👑", "desc": "Earned 500+ academic karma", "min_karma": 500}
}

TIERS = [
    {"name": "Novice Scholar", "min_karma": 0, "color": "#718096"},
    {"name": "Apprentice Scholar", "min_karma": 50, "color": "#3182CE"},
    {"name": "Senior Contributor", "min_karma": 150, "color": "#38A169"},
    {"name": "Distinguished Fellow", "min_karma": 300, "color": "#805AD5"},
    {"name": "Academic Grandmaster", "min_karma": 600, "color": "#D69E2E"}
]

def calculate_tier(karma: int) -> dict:
    """Determine the user tier based on karma points."""
    current_tier = TIERS[0]
    for tier in TIERS:
        if karma >= tier["min_karma"]:
            current_tier = tier
        else:
            break
    return current_tier

def evaluate_badges(user_profile: dict, upload_count: int, avg_rating: float = 0.0) -> list:
    """Evaluate earned badges for a user based on metrics."""
    earned = []
    karma = user_profile.get("karma", 0)
    
    if upload_count >= BADGE_DEFINITIONS["FIRST_UPLOAD"]["min_uploads"]:
        earned.append("FIRST_UPLOAD")
    if upload_count >= BADGE_DEFINITIONS["PROLIFIC_AUTHOR"]["min_uploads"]:
        earned.append("PROLIFIC_AUTHOR")
    if upload_count >= BADGE_DEFINITIONS["COMMUNITY_PILLAR"]["min_uploads"]:
        earned.append("COMMUNITY_PILLAR")
    if karma >= BADGE_DEFINITIONS["KARMA_CENTURION"]["min_karma"]:
        earned.append("KARMA_CENTURION")
    if karma >= BADGE_DEFINITIONS["CAMPUS_LEGEND"]["min_karma"]:
        earned.append("CAMPUS_LEGEND")
    if avg_rating >= BADGE_DEFINITIONS["TOP_RATED"]["min_rating"] and upload_count >= 2:
        earned.append("TOP_RATED")
        
    return earned

def build_leaderboard(users_db: dict, limit: int = 10) -> list:
    """Generate sorted leaderboard ranking from users database."""
    board = []
    for uname, data in users_db.items():
        if data.get("role") == "faculty":
            continue
        karma = data.get("karma", 0)
        tier = calculate_tier(karma)
        board.append({
            "username": uname,
            "name": data.get("name", uname),
            "branch": data.get("branch", "General"),
            "karma": karma,
            "tier": tier["name"],
            "badges_count": len(data.get("badges", []))
        })
    board.sort(key=lambda x: x["karma"], reverse=True)
    for rank, entry in enumerate(board, start=1):
        entry["rank"] = rank
    return board[:limit]
