import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(hashed_password.encode(), password.encode())
