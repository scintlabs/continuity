# API Routes

This document outlines the REST endpoints defined in `base/api/routes.py`. The module uses FastAPI and exposes a small set of write-focused routes. Each endpoint accepts a Pydantic model and is currently a stub (the body is elided with `...`).

## Endpoints

| Method | Path | Handler | Request model | Description |
|--------|------|---------|---------------|-------------|
| `POST` | `/ingest` | `ingest_endpoint` | `IngestRequest` | Ingest a piece of text or other content. |
| `POST` | `/classify` | `classify_endpoint` | `IngestRequest` | Classify an item that has been ingested. |
| `POST` | `/context` | `context_endpoint` | `QueryRequest` | Retrieve context related to a query. |
| `POST` | `/knowledge` | `knowledge_endpoint` | `IngestRequest` | Persist extracted knowledge from text. |
| `POST` | `/preferences` | `preferences_endpoint` | `IngestRequest` | Update a user's preferences. |

### Request Models

`IngestRequest` (from `base.schema.requests`) has the following fields:

```python
class IngestRequest(BaseModel):
    text: str
    type: str = "message"
```

`QueryRequest`:

```python
class QueryRequest(BaseModel):
    text: str
    k: int = 8
    type: str | None = None
```

### Return Types

Each handler currently uses the placeholder `...` and does not specify a concrete return type. In a full implementation you would expect a JSON response (FastAPI will automatically serialize the returned Python objects). Until implemented, these endpoints effectively return `None`.

### Interaction with Other Modules

Routes import these schemas from `base.schema.requests`. The router itself is included in `base/api/main.py` via `api_router.include_router(routes.router)`. Outside of schema usage, there are no other dependencies in `routes.py`.

