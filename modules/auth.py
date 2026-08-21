import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_credentials(users_db: dict, username: str, password_plain: str) -> tuple:
    uname = username.strip().lower()
    if uname not in users_db:
        return False, 'Account does not exist.'
    if hash_password(password_plain) != users_db[uname].get('password'):
        return False, 'Incorrect password.'
    return True, users_db[uname]
