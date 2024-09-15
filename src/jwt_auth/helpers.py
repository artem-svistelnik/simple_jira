from cryptography.fernet import Fernet
from app.core.config import settings


def hash_password(password):
    encrypted = Fernet(settings.SECRET_KEY).encrypt(password.encode()).decode()
    return encrypted


def unhash_password(hashed_password):
    decrypted = Fernet(settings.SECRET_KEY).decrypt(hashed_password).decode()
    return decrypted


def verify_password(login_dta_password, password):
    return unhash_password(password) == login_dta_password
