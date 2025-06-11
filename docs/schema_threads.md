# Thread and Conversation Models

This document summarizes the data models defined in `base/schema/threads.py`.

## ThreadTransition

`ThreadTransition` is an `Enum` describing lifecycle events for a thread. Each
value holds a timestamped dictionary. Available states are `CREATED`, `ENCODED`,
`ARCHIVED`, and `PRUNED`.

```python
class ThreadTransition(Enum):
    CREATED  = {"created":  lambda: timestamp()}
    ENCODED  = {"encoded":  lambda: timestamp()}
    ARCHIVED = {"archived": lambda: timestamp()}
    PRUNED   = {"pruned":   lambda: timestamp()}
```

The enum instances are callable, returning the event record with an optional
`content` field. Threads record these events to their attached `Metadata`.

## Thread

`Thread` represents a unit of conversation. It stores the actual message
content and links to previous/next threads forming a doubly linked list.

Important fields:

- `content: List[Content]` – messages in the thread
- `prev: Optional[Thread]` – link to the previous thread
- `next: Optional[Thread]` – link to the next thread

The `update` method appends new content and can store an embedding on its
`Metadata`. `transition()` creates a new thread instance using `_NEXT` and adds
an event specified by `_EVENT_AFTER`.

Threads rely on a `Metadata` object (from `base.schema.context`) to record
events and embeddings. This metadata integrates with the broader context
management utilities in `base/core/context.py` which generate summaries and
maintain embeddings.

## Threads container

`Threads` manages a collection of `Thread` objects. It keeps `head` and `tail`
pointers and maintains counts for different thread types. Key configuration
attributes include:

- `maxlen` – maximum number of active `Thread` instances
- `index_threshold` – length before stale threads are advanced
- `encode_threshold` – limit for encoded threads before pruning
- `should_index` – callback deciding if a thread should be removed from the list

The container supports `append` and `pop` operations, with automatic rollover to
manage memory. When a new thread is appended the container records an
`ACTIVATED` event (via `ThreadTransition`) and calls `_maybe_rollover` to enforce
limits.

Internally, methods such as `_index`, `_advance_stale`, and `_replace` help move
threads through different lifecycle states and update their metadata.

## Relation to Context Management

Threads capture conversational slices and their metadata provides summaries and
embeddings for context retrieval. The `Metadata` class (see
`base/core/context.py`) defines fields like `thread_id`, `summary`, and
`embedding`. Thread methods update this metadata, enabling context generation
and efficient retrieval of related threads.

`Threads` thus acts as the backbone for organizing conversations while the
context system leverages the stored metadata to produce high level summaries and
maintain conversational memory.
