# Core Library

This document describes the minimal data structures and helper utilities found in `base/core/library.py` and related modules.

## Load Instructions

`load_instructions(name: str)` reads `config/instructions.json` and returns the `content` field for the object whose `name` matches the provided value. The JSON file contains an array of instruction definitions. Example:

```json
[
  { "name": "default", "content": "You are a helpful assistant." },
  { "name": "friendly", "content": "You are a friendly assistant." }
]
```

Use this helper to retrieve system prompts for a particular style or persona.

## `Library` Dataclass

```python
@define
class Library:
    preferences: Dict[str, Callable] = field(factory=dict)

    async def load(self, id: str): ...
    async def search(self, query: str, category: str): ...
```

`Library` stores preference handlers keyed by name. The `load` method is intended to populate the library for a given user or session. `search` is a stub for querying stored objects.

## Repository for Outlines and Tools

The module `base/core/repository.py` defines a simple in-memory repository for outlines and tools:

```python
@define
class Repository:
    outlines: Dict[str, Any] = field(factory=dict)
    tools: Dict[str, Any] = field(factory=dict)
    ...
```

It exposes CRUD methods (`add_`, `get_`, `update_`, `delete_`) for both outlines and tools, along with `list_outlines()` and `list_tools()` helpers. These structures can be used by `Library` implementations to organise reusable conversation outlines and callable tools.

## Typical Usage

1. Define instruction presets in `config/instructions.json`.
2. Use `load_instructions("friendly")` to fetch a prompt tailored for a friendly assistant.
3. Implement a `Library` subclass that overrides `load` and `search` to retrieve outlines and tools from a `Repository` instance or another storage backend.
4. Register preference functions under `Library.preferences` to customise behaviour per user.

`Library`, together with the repository utilities, forms the basis for storing and retrieving conversation outlines, tool definitions and preference logic within the application.
