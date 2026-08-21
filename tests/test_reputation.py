from modules.reputation import get_karma_tier

def test_tiers():
    assert 'Faculty Lead' in get_karma_tier(150)
    assert 'Senior Contributor' in get_karma_tier(60)
    assert 'Verified Student' in get_karma_tier(10)
