from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    ROOT_DIR: Path = Path(__file__).parent.parent.resolve()

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "user"
    POSTGRES_DB: str = "db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    IS_DEBUG: bool = False

    @computed_field
    def dsn(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.POSTGRES_DB}"
        )


config = Config()
