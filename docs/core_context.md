# Context Class

This document describes the small `Context` container defined in
`base/core/context.py`.  The module provides a lightweight structure for
storing a message along with optional header information and metadata.

## Structure

`Context` and its helper classes are `attrs` dataclasses.

```python
@define
class Header:
    sender_id: str = field(default=None)
    thread_id: str = field(default=None)

@define
class Metadata:
    thread_id: str = field(default=None)
    summary: str = field(default=None)
    embedding: List[float] = field(default=None)

@define
class Context:
    header: Header = field(default=None)
    metadata: Metadata = field(default=None)
    content: Content
```

The `content` field holds the actual message payload.  `Header` contains basic
routing details, while `Metadata` stores a summary and vector embedding for the
conversation.

## Rendering and Metadata

`Metadata.metadata` is a class method that triggers language model generation of
a metadata block.  It assumes that the class (or a subclass) implements
`render()` to output the thread text and `serialize()` to return a JSON schema.
It then calls `generate()` from `base.core.classify`:

```python
res = await generate(
    input=f"Generate concise, intelligent, semantically-rich metadata for the "
          f"following thread:\n\n{await cls.render()}",
    text={"format": serialize(Metadata)},
    model="gpt-4.1",
)
```

Each returned message is parsed as JSON and used to instantiate `Metadata`.
The helper `serialize` (from `base.helpers`) builds a schema for the data class
so that the language model returns structured JSON.

The module defines a constant `SIMILARITY_THRESHOLD = 0.85`, which can be used
when comparing embeddings to decide if two pieces of text are related.

## Example

```python
from base.core.context import Context, Header, Metadata
from base.schema.messages import Content

ctx = Context(
    header=Header(sender_id="u123", thread_id="t1"),
    metadata=Metadata(summary="Initial question"),
    content="How does the system handle context?",
)
```

In practice, subclasses may implement `render()` to provide a textual
representation of the thread so that `Metadata.metadata()` can build a summary
and embedding.

