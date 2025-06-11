import os
import secrets
from typing import Annotated, Any, Literal

from openai import AsyncOpenAI

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PG_SERVER: str
    PG_PORT: int = 5432
    PG_USER: str
    PG_PW: str = ""
    PG_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.PG_USER,
            password=self.PG_PW,
            host=self.PG_SERVER,
            port=self.PG_PORT,
            path=self.PG_DB,
        )

    postgres = os.environ.get(
        "PG_DSN", "postgresql://postgres:postgres@postgres:5432/memdb"
    )

    QDRANT_URL = os.environ.get("QDRANT_URL", "")
    QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    REDIS_STREAM_KEY = "memory_ingest"
    EMBED_API = "https://api.openai.com/v1/embeddings"
    EMBED_MODEL = "text-embedding-3-small"
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


settings = Settings()

OPENAI_CLIENT = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
