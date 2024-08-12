from typing import Iterator

import pytest
from alembic.config import Config
from utils import make_alembic_config, tmp_database

from core.settings import config


@pytest.fixture
def postgres(pg_url: str) -> Iterator[str]:
    """
    Creates empty temporary database.
    """
    with tmp_database(pg_url, suffix="migrations") as tmp_url:
        yield tmp_url


@pytest.fixture
def alembic_config(postgres: str) -> Config:
    """
    Alembic configuration object, bound to temporary database.
    """
    return make_alembic_config(postgres, "app")