from __future__ import annotations

from typing import Any, Dict, List

from attrs import define, field
from chonkie import RecursiveChunker


async def embed(input: str):
    req = {"model": "text-embedding-3-small", "input": str(input)}
    res = await OPENAI_CLIENT.embeddings.create(**req)
    return res.data[0].embedding


def chunk_markdown(input: str):
    chunker = RecursiveChunker().from_recipe("markdown")
    chunks = chunker(input)

    for i, chunk in enumerate(chunks):
        chunk.metadata = {
            "chunk_id": f"ai_text_chunk_{i+1:03d}",
            "source": "AI overview article",
        }

    return chunks


@define
class Indexes:
    client: None = field(None)
    indexes: Dict[str, Any] = field(factory=dict)

    async def load_indexes(self, index_names: List[str]): ...
    async def get_index(self, name: str): ...
    async def delete_index(self, name: str): ...
    async def add_records(self, records: List[Dict[str, Any]]): ...
    async def delete_records(self, document_ids: List[str]): ...
