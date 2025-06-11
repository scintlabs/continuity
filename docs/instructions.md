# Instructions Format

Instructions for the library live in `config/instructions.json`. The file is a JSON array where each object provides the instruction text for a given name.

```json
[
  {
    "name": "default",
    "content": "You are a helpful assistant. Keep responses short and direct."
  }
]
```

Use `load_instructions(name)` to retrieve the `content` for a matching `name`.
