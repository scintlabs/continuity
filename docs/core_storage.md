# Core Storage Overview

`base/core/storage.py` sets up the SQL database connection and defines
`init_db` for creating tables.

## Engine Setup

```python
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
```

The engine uses the `SQLALCHEMY_DATABASE_URI` from `base.config.Settings`.
This URI points to the Postgres instance used by the application.

## `init_db`

```python
def init_db(session: Session) -> None:
    """Initialise the database tables."""
    SQLModel.metadata.create_all(engine)
```

- Accepts a SQLModel `Session` (currently unused).
- Calls `SQLModel.metadata.create_all(engine)` to create any tables for
  SQLModel models that have been imported.
- Table definitions are gathered from model classes across the codebase;
  when new models are added, running `init_db` will create the missing
  tables if they do not already exist.
- Currently the repository includes no SQLModel models, so `init_db` will create no tables until models are added.
