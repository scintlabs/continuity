from __future__ import annotations

import random
from typing import Any

from base.config import OPENAI_CLIENT


async def classify(obj: Any, kind: str, /, val: str | None = None) -> str | None:
    """Classify ``obj`` using the configured OpenAI client.

    Parameters
    ----------
    obj : Any
        The object or text being classified.
    kind : str
        Either ``"parameter"`` or ``"thread"`` to determine the
        prompt template used.
    val : str, optional
        The name of the parameter when ``kind`` is ``"parameter"``.

    Returns
    -------
    str | None
        The generated text returned by OpenAI or ``None`` if no text
        was produced.
    """

    req = {
        "model": "o4-mini",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
    }
    if kind == "parameter":
        msg = f"{val} is a parameter for the following function:\n\n{obj}\n\nPlease generate a single sentence describing the parameter."
        req["input"] = msg
    if kind == "thread":
        msg = "Generate a name and description for this conversation, which is used to populate the class object's `name` and `description` fields. Simple provide a concise name in the form of a title and a one-sentence description. Return the name on the first line and the description on the second line."
        req["input"] = f"{msg}\n\n{obj}"

    res = await OPENAI_CLIENT.responses.create(**req)
    if res.output_text is not None:
        return res.output_text
