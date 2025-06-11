# Message Schema

`base/schema/messages.py` defines several simple data containers for different message types. They are implemented with the [`attrs`](https://www.attrs.org/) library using `@define` and `field`.

## Shared `Content` alias

```python
Content: TypeAlias = Union[str, bytes, list, dict]
```

`Content` represents the payload for all messages and can be text (`str`), binary (`bytes`), a `list`, or a `dict`.

## Message classes

Each class only stores an identifier and the `Content`. All fields are optional and default to `None`.

| Class          | Fields                                     |
|----------------|--------------------------------------------|
| `Request`      | `id: str` – request identifier<br>`content: Content` – message body |
| `Response`     | `id: str` – response identifier<br>`content: Content` – message body |
| `Message`      | `id: str` – message identifier<br>`content: Content` – message body |
| `Command`      | `id: str` – command identifier<br>`content: Content` – message body |
| `Notification` | `id: str` – notification identifier<br>`content: Content` – message body |
| `Instructions` | `id: str` – instructions identifier<br>`content: Content` – instructions payload |

These structures have no additional methods; they are plain data holders used throughout the library to represent various kinds of events or API inputs/outputs.
