import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import bcrypt

def hash_password(password):
    """Hashes the password using bcrypt and generates a salt."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Base64 encode salt for easy storage and retrieval
    salt_encoded = base64.urlsafe_b64encode(salt).decode('utf-8')
    return password_hash.decode('utf-8'), salt_encoded

def verify_password(stored_password, provided_password, salt):
    """Verifies the provided password using PBKDF2HMAC and bcrypt."""
    decoded_salt = base64.urlsafe_b64decode(salt.encode('utf-8'))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=decoded_salt,
        iterations=100000,
        backend=default_backend()
    )
    try:
        bcrypt.checkpw(provided_password.encode(), stored_password.encode())
        return True
    except Exception as e:
        return False

class User:
    def __init__(self, name, email, password, mobile):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.password_hash, self.salt = hash_password(password)