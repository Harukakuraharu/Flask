import bcrypt
from errors import HttpError
from flask_jwt_extended import current_user
from models.models import MODEL


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_owner(model: MODEL, item_id: int)-> bool:
    item = model.query.filter_by(id=item_id).one_or_none()
    if item.user_id != current_user.id:
        raise HttpError(401, "Has no permission")
