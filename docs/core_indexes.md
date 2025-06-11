# Indexes Module

This document summarizes `base/core/indexes.py` and explains the intended vector storage
approach for the project.

## Purpose

The file defines helpers for creating embeddings and slicing text into
document chunks. It also declares an `Indexes` dataclass that will manage
vector indexes.

## Embedding

```python
async def embed(input: str):
    req = {"model": "text-embedding-3-small", "input": str(input)}
    res = await OPENAI_CLIENT.embeddings.create(**req)
    return res.data[0].embedding
```

- Embeddings are generated with the OpenAI client using the
  `text-embedding-3-small` model.
- The function returns the numeric vector from the first result.

## Chunking Markdown

```python
def chunk_markdown(input: str):
    chunker = RecursiveChunker().from_recipe("markdown")
    chunks = chunker(input)

    for i, chunk in enumerate(chunks):
        chunk.metadata = {
            "chunk_id": f"ai_text_chunk_{i+1:03d}",
            "source": "AI overview article",
        }

    return chunks
```

- Uses the `RecursiveChunker` from `chonkie` to break markdown text into
  pieces.
- Each piece gets a simple metadata dictionary with a generated chunk id.

## `Indexes` Dataclass

The dataclass stores a reference to a client (likely a vector DB client)
plus a dictionary of indexes. Its methods—`load_indexes`, `get_index`,
`delete_index`, `add_records`, and `delete_records`—are declared but not
implemented.

```python
@define
class Indexes:
    client: None = field(None)
    indexes: Dict[str, Any] = field(factory=dict)
    async def load_indexes(self, index_names: List[str]): ...
    async def get_index(self, name: str): ...
    async def delete_index(self, name: str): ...
    async def add_records(self, records: List[Dict[str, Any]]): ...
    async def delete_records(self, document_ids: List[str]): ...
```

## Storage Back‑Ends

The implementation is incomplete, but the wider repository indicates the
following storage components:

- **Qdrant** – used as a vector store for embeddings, as described in
  `docs/architecture.md`.
- **Postgres** – stores metadata such as threads and events.
- **Redis** – provides caching and stream queues.

Currently `indexes.py` does not contain logic for inserting or querying
embeddings, so the exact interaction with Qdrant or other stores is not
yet defined.
