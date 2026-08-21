from modules.auth import hash_password, verify_credentials

def test_hash_consistency():
    assert hash_password('abc') == hash_password('abc')
    assert len(hash_password('abc')) == 64

def test_verify_credentials():
    db = {'u1': {'password': hash_password('123'), 'name': 'User One'}}
    ok, data = verify_credentials(db, 'u1', '123')
    assert ok is True
    assert data['name'] == 'User One'
