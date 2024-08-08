from typing import Optional, Type

import pydantic


class BaseUser(pydantic.BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is too short")
        return value


class BaseAdvertisement(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]


class CreateUser(BaseUser):
    name: str
    password: str


class CreateAdvertisement(BaseAdvertisement):
    title: str
    description: str
    user_id: int


class UpdateAdvertisement(BaseAdvertisement):
    title: Optional[str] = None
    description: Optional[str] = None


Schema = Type[CreateUser] | Type[CreateAdvertisement] | Type[UpdateAdvertisement]
