from __future__ import annotations

import json
from typing import Callable, Dict

from attrs import define, field


def load_instructions(name: str):
    with open("config/instructions.json", "r") as f:
        content = f.read()
        for i in json.loads(content):
            if i.get("name") == name.lower():
                return i.get("content")


@define
class Library:
    preferences: Dict[str, Callable] = field(factory=dict)

    async def load(self, id: str): ...
    async def search(self, query: str, category: str): ...
