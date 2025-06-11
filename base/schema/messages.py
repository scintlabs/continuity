from __future__ import annotations

from typing import TypeAlias, Union

from attrs import define, field


@define
class Request:
    id: str = field(default=None)
    content: Content = field(default=None)


@define
class Response:
    id: str = field(default=None)
    content: Content = field(default=None)


@define
class Message:
    id: str = field(default=None)
    content: Content = field(default=None)


@define
class Command:
    id: str = field(default=None)
    content: Content = field(default=None)


@define
class Notification:
    id: str = field(default=None)
    content: Content = field(default=None)


@define
class Instructions:
    id: str = field(default=None)
    content: Content = field(default=None)


Content: TypeAlias = Union[str, bytes, list, dict]
