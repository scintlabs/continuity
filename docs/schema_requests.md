## Request Schemas

`base/schema/requests.py` defines the small set of request models shared across the API. They are simple Pydantic `BaseModel` classes used for validating incoming JSON payloads.

### `IngestRequest`

Fields:

- `text` (`str`): raw text to ingest.
- `type` (`str`, default `"message"`): optional label for the data being stored.

This model is used by the ingestion oriented endpoints such as `/ingest`, `/classify`, `/knowledge`, and `/preferences`.

### `QueryRequest`

Fields:

- `text` (`str`): the search text or prompt used to retrieve context.
- `k` (`int`, default `8`): number of similar items to return.
- `type` (`str | None`, optional): filter for a specific item type.

This model is used by the read‑only `/context` endpoint. Both models may expand as the API grows but currently serve as straightforward containers for request data.
