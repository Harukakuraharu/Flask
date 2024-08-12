from typing import Any

import sqlalchemy as sa
from core.db import db
from errors import HttpError
from models.models import MODEL
from sqlalchemy.exc import IntegrityError


def get_data(item_id: int, model: MODEL):
    stmt = sa.select(model).where(model.id == item_id)
    result = db.session.scalar(stmt)
    if result is None:
        raise HttpError(404, f"{model.__name__} not found")
    return result


def add_data(model: MODEL, data: dict[str, Any]):
    stmt = sa.insert(model).values(**data).returning(model)
    try:
        model_db = db.session.scalar(stmt)
        db.session.commit()
    except IntegrityError as error:
        raise HttpError(400, f"{model.__name__} already exists") from error
    return model_db


def update_data(model: MODEL, data: dict[str, Any]):
    item_id = data.pop("id")
    stmt = sa.update(model).values(**data).where(model.id == item_id).returning(model)
    model_db = db.session.scalar(stmt)
    db.session.commit()
    return model_db


def delete_item(model: MODEL, item_id: int):
    stmt = sa.delete(model).where(model.id == item_id)
    db.session.execute(stmt)
    db.session.commit()
