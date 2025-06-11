from __future__ import annotations

from typing import Any, Dict

from attrs import define, field


@define
class Repository:
    outlines: Dict[str, Any] = field(factory=dict)
    tools: Dict[str, Any] = field(factory=dict)
