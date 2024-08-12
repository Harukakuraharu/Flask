from typing import Annotated, Type

import pydantic
from pydantic import EmailStr
from pydantic.functional_validators import AfterValidator


def secure_password(password: str):
    assert len(password) >= 8, "Password is too short"
    return password


Password = Annotated[str, AfterValidator(secure_password)]


class BaseUser(pydantic.BaseModel):
    name: str
    email: EmailStr


class CreateUser(BaseUser):
    password: Password


class ResponseUser(BaseUser):
    id: int


class BaseAdvertisement(pydantic.BaseModel):
    title: str
    description: str
    user_id: int


class CreateAdvertisement(BaseAdvertisement):
    pass


class ResponseAdvertisement(BaseAdvertisement):
    id: int


class UpdateAdvertisement(pydantic.BaseModel):
    title: str | None = None
    description: str | None = None


Schema = (
    Type[CreateUser]
    | Type[ResponseUser]
    | Type[CreateAdvertisement]
    | Type[ResponseAdvertisement]
    | Type[UpdateAdvertisement]
)
