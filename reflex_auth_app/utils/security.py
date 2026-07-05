import bcrypt
import random

AVATAR_COLORS = [
    "#4F46E5",  # índigo
    "#7C3AED",  # violeta
    "#DB2777",  # rosa
    "#DC2626",  # rojo
    "#D97706",  # ámbar
    "#059669",  # esmeralda
    "#0284C7",  # azul cielo
    "#0891B2",  # cyan
    "#65A30D",  # lima
    "#9333EA",  # púrpura
]

def generate_avatar_color() -> str:
    return random.choice(AVATAR_COLORS)

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)



