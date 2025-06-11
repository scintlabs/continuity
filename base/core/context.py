from __future__ import annotations

import json
from typing import List

from attrs import define, field

from base.core.classify import generate
from base.helpers import serialize
from base.schema.messages import Content

SIMILARITY_THRESHOLD = 0.85


@define
class Header:
    sender_id: str = field(default=None)
    thread_id: str = field(default=None)


@define
class Metadata:
    thread_id: str = field(default=None)
    summary: str = field(default=None)
    embedding: List[float] = field(default=None)

    @classmethod
    async def metadata(cls):
        """Generate and parse metadata for the current context.

        The method assumes ``cls.render`` produces the text representation of
        the conversation and ``cls.serialize`` yields a JSON schema describing
        :class:`Metadata`. The ``generate`` helper returns an object whose
        ``output`` contains JSON fragments that can be loaded into this class.
        """
        res = await generate(
            input=f"Generate concise, intelligent, semantically-rich metadata for the following thread:\n\n{await cls.render()}",
            text={"format": serialize(Metadata)},
            model="gpt-4.1",
        )

        for obj in res.output:
            if obj.type == "message":
                for content in obj.content:
                    text = json.loads(content.text)
                    return cls(**text)


@define
class Context:
    header: Header = field(default=None)
    metadata: Metadata = field(default=None)
    content: Content
