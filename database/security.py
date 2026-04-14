import hashlib 
from werkzeug.security import generate_password_hash, check_password_hash

def secure(data):
    return generate_password_hash(data)

def check_password(password, hash):
    return check_password_hash(hash, password)
