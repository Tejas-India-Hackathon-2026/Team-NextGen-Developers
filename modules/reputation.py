KARMA_REWARDS = {'approved': 10, 'upvote': 2, 'rejected': -10, 'spam': -20}

def get_karma_tier(points: int) -> str:
    if points >= 100: return '🌟 Faculty Lead'
    if points >= 50: return '💎 Senior Contributor'
    if points >= 25: return '🥈 Active Contributor'
    return '🥉 Verified Student'
