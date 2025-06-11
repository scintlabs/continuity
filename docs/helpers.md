# Helper Utilities

This file documents the utility helpers available in `base/helpers.py`.

| Helper | Purpose |
|--------|---------|
| `_quote(value: str)` | Escape single quotes in a string. |
| `_json_dumps(obj)` | Serialize an object to compact JSON. |
| `timestamp()` | Return the current timestamp formatted as `%A, %B %d, %Y @ %H:%M`. |
| `timestamp_to_epoch(ts)` | Convert a formatted timestamp string to Unix epoch seconds. |
| `iso_to_epoch(ts)` | Convert an ISO timestamp to UTC epoch seconds. |
| `cosine_similarity(vec_a, vec_b)` | Compute the cosine similarity between two numeric vectors. |
| `generate_hash(file_path)` | SHA-256 hash of a file, streaming when files exceed 1MB. |
| `env(var)` | Load `.env` and return the given environment variable. |
| `import_object(module_path, obj_name)` | Import an object by module path and name. |
| `_json_type(tp)` | Map Python annotations to a JSON schema fragment. |
| `_param_docs(func)` | Parse parameter descriptions from a function docstring. |
| `_func_schema(func)` | Build a JSON schema for a function's parameters. |
| `_type_schema(cls)` | Construct a JSON schema for an `attrs` class. |
| `serialize(obj)` | Serialize a function or class to a structured representation. |
| `Primitive` | Enum providing JSON schema templates for primitive types. |

`base/helpers.py` also defines `_DEFAULT_BASELINE`, a tuple of initial SQL
statements used elsewhere in the project.
