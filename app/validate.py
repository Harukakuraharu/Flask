import pydantic
from errors import HttpError
from schema import Schema


def validate(schema_cls: Schema, json_data: dict):
    """
    Функция для валидации данных, принимает класс пайдантика, который валидирует данные. Возвращает отвалидированные данные
    """
    try:
        return schema_cls.model_validate_json(json_data)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)
