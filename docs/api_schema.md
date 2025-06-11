# API Schemas

The API exposes a handful of endpoints under `base/api/routes.py`. Each route
expects a Pydantic model defined in the API's schema modules. These classes act
as typed containers for the incoming JSON payloads.

## Request models

`base/api/schema.py` declares four placeholder models:

- **`IngestRequest`** – payload for new content that should be stored or
  processed.
- **`ContextRequest`** – request for pulling conversation context.
- **`KnowledgeRequest`** – used by the knowledge ingestion endpoint.
- **`ClassificationRequest`** – request body for classification operations.

The actual field definitions live in `base/schema/requests.py` and are imported
by the routes. They provide the concrete attributes used at runtime:

```python
class IngestRequest(BaseModel):
    text: str
    type: str = "message"

class QueryRequest(BaseModel):
    text: str
    k: int = 8
    type: str | None = None
```

## Mapping to routes

`base/api/routes.py` binds these models to specific endpoints:

- `POST /ingest`, `POST /knowledge` and `POST /preferences` consume an
  `IngestRequest`.
- `POST /classify` also receives an `IngestRequest`.
- `POST /context` accepts a `QueryRequest` to search for related threads.

These schemas ensure each endpoint receives a predictable JSON structure with
sensible defaults.
