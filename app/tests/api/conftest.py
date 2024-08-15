from typing import Callable, Iterator
from urllib.parse import urlsplit

import pytest
import sqlalchemy as sa
from core.db import Base
from core.settings import config
from faker import Faker
from models.models import MODEL, User
from security import hash_password
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from utils import tmp_database

from app import create_app
from flask.testing import FlaskClient
from flask import Flask

@pytest.fixture(scope="session", autouse=True)
def postgres_temlate(pg_url: str) -> Iterator[str]:
    """
    Creates empty template database with migrations.
    """
    with tmp_database(pg_url, db_name="api_template") as tmp_url:
        engine = sa.create_engine(tmp_url)
        Base.metadata.create_all(bind=engine)
        engine.dispose()
        yield tmp_url


@pytest.fixture
def postgres(postgres_temlate: str) -> Iterator[str]:
    """
    Creates empty temporary database.
    """
    with tmp_database(
        postgres_temlate, suffix="api", template="api_template"
    ) as tmp_url:
        yield tmp_url


@pytest.fixture
def app(postgres: str) -> Iterator[Flask]:
    config.POSTGRES_DB = urlsplit(postgres).path[1:]
    project_app = create_app(config.dsn)
    project_app.config.update(
        {
            "TESTING": True,
        }
    )

    yield project_app


@pytest.fixture
def client(app: Flask)-> FlaskClient:
    return app.test_client()


@pytest.fixture
def fakery()-> Faker:
    return Faker()


@pytest.fixture
def session(postgres: str) -> Iterator[Session]:
    with Session(create_engine(postgres)) as session:
        yield session


@pytest.fixture
def factory(session: Session):
    def wrapper(model: MODEL, *args, **kwargs):
        instance = model(*args, **kwargs)
        session.add(instance)
        session.commit()
        return instance

    return wrapper


@pytest.fixture
def user_factory(session: Session, factory: Callable, fakery: Faker, client: FlaskClient) -> dict:
    def wrapper():
        password = fakery.password()
        email = fakery.email()
        user = factory(User, email=email, password=password, name=fakery.first_name())
        user.password = hash_password(user.password)
        session.commit()
        response = client.post("/login", json={"email": email, "password": password})
        token = response.json.get("access_token")
        return {"user": user, "password": password, "token": token}

    return wrapper
