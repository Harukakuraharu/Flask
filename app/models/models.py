import datetime
from typing import Annotated

from core.db import db
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

idpk = Annotated[int, mapped_column(primary_key=True)]


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[idpk]
    name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[str] = mapped_column(String(72))
    advertisement: Mapped[list["Advertisement"]] = relationship(
        "Advertisement", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


class Advertisement(db.Model):
    __tablename__ = "advertisement"

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, back_populates="advertisement")

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "user_id": self.user_id,
        }


MODEL = User | Advertisement

