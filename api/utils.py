# filepath: /c:/Users/Zayen/OneDrive/Desktop/Aziza Othmana API/medical_api/api/utlis.py
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False