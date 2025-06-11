# Core Repository

This module defines a lightweight in-memory registry used by the rest of the library. It stores **outlines** and **tools** in simple dictionaries and exposes helper methods for common CRUD operations.

## Data Model

```python
@define
class Repository:
    outlines: Dict[str, Any] = field(factory=dict)
    tools: Dict[str, Any] = field(factory=dict)
```
- `outlines` and `tools` hold arbitrary objects indexed by a name.
- Data is not persisted to disk or a database; once a `Repository` instance is discarded, its contents are lost.

## CRUD Helpers

The class provides small methods to manage each collection:

| Method | Purpose |
|-------|---------|
| `add_outline(name, outline)` | Insert a new outline. |
| `get_outline(name)` | Retrieve an outline by name, or `None` if missing. |
| `update_outline(name, outline)` | Replace or create an outline. |
| `delete_outline(name)` | Remove an outline if it exists. |
| `list_outlines()` | Return a list of all outline names. |
| `add_tool(name, tool)` | Insert a new tool. |
| `get_tool(name)` | Retrieve a tool by name. |
| `update_tool(name, tool)` | Replace or create a tool. |
| `delete_tool(name)` | Remove a tool if present. |
| `list_tools()` | Return a list of all tool names. |

Each helper simply interacts with the underlying dictionary. There are no higher-level query abstractions or database logic. The repository acts as a straightforward in-memory store meant for prototyping or unit tests.
