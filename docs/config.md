# Configuration

This project stores runtime settings in `base/config.py`. Settings are defined with `pydantic.BaseSettings`, so values can be supplied via environment variables or a `.env` file.

## Environment variables

- `PG_SERVER` – Postgres host.
- `PG_PORT` – defaults to `5432`.
- `PG_USER` – Postgres user name.
- `PG_PW` – defaults to an empty string.
- `PG_DB` – defaults to an empty string.
- `PG_DSN` – optional DSN with default `postgresql://postgres:postgres@postgres:5432/memdb`.
- `QDRANT_URL` – vector store endpoint, default empty string.
- `QDRANT_API_KEY` – optional API key.
- `REDIS_URL` – defaults to `redis://localhost:6379/0`.
- `OPENAI_API_KEY` – required by the OpenAI client.

## Defaults and constants

Some values have in-code defaults:

- `API_V1_STR` – `"/api/v1"`.
- `SECRET_KEY` – generated with `secrets.token_urlsafe`.
- `ACCESS_TOKEN_EXPIRE_MINUTES` – `60 * 24 * 8`.
- `PROJECT_NAME` – `"Continuity"`.
- `FRONTEND_HOST` – `"http://localhost:5173"`.
- `ENVIRONMENT` – `"local"`.
- `BACKEND_CORS_ORIGINS` – empty list by default.
- `REDIS_STREAM_KEY` – `"memory_ingest"`.
- `EMBED_API` – `"https://api.openai.com/v1/embeddings"`.
- `EMBED_MODEL` – `"text-embedding-3-small"`.

`SQLALCHEMY_DATABASE_URI` is computed from the Postgres parameters above.

## Global objects

The module instantiates a few objects when imported:

- `OPENAI_CLIENT` – `AsyncOpenAI` configured with `settings.OPENAI_API_KEY`.
- `settings` – instance of `Settings` providing all resolved values.

