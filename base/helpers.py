from __future__ import annotations

import hashlib
import inspect
import json
import os
import textwrap
from datetime import datetime as dt
from datetime import timezone as tz
from enum import Enum
from importlib import import_module
from typing import Any, Dict, Generic, List, TypeVar, Union

import attrs
import dotenv
from typing_extensions import get_args, get_origin

P = TypeVar("P")
T = TypeVar("T")

TS_FMT = "%A, %B %d, %Y @ %H:%M"


_DEFAULT_BASELINE: tuple[str, ...] = (
    "CREATE NODE TABLE Generic(id STRING, props STRING, PRIMARY KEY(id))",
    "CREATE REL TABLE RELATED(FROM Generic TO Generic, props STRING)",
)


def _quote(value: str) -> str:
    return value.replace("'", "\\'")


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"))


def timestamp():
    current_time = dt.now().astimezone()
    return current_time.strftime(TS_FMT)


def timestamp_to_epoch(ts: str):
    return dt.strptime(ts, TS_FMT).timestamp()


def iso_to_epoch(ts: str):
    return dt.fromisoformat(ts).astimezone(tz.utc).timestamp()


def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)


def generate_hash(file_path):
    if os.path.getsize(file_path) > 1e6:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_String in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_String)
            return sha256_hash.hexdigest()
    with open(file_path, "rb") as f:
        data = f.read()
        readable_hash = hashlib.sha256(data).hexdigest()
    return readable_hash


def env(var: str):
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


def import_object(module_path: str, obj_name: str):
    module = import_module(module_path)
    return getattr(module, obj_name)


_IGNORED = {
    "namespace",
    "base_id",
    "base_ns",
    "kind",
    "created",
    "metadata",
    "_reply_future",
}


def _json_type(tp: Any):
    primitives = {str: "string", int: "integer", float: "number", bool: "boolean"}
    origin, args = get_origin(tp), get_args(tp)

    if origin is Union and type(None) in args:
        return _json_type([a for a in args if a is not type(None)][0])

    if origin in {list, List}:
        return {"type": "array", "items": _json_type(args[0] if args else str)}

    if origin in {dict, Dict}:
        return {"type": "object"}

    if isinstance(tp, type) and issubclass(tp, Enum):
        return {"type": "string", "enum": [e.name for e in tp]}

    return {"type": primitives.get(tp, "string")}


def _param_docs(func):
    doc = textwrap.dedent(inspect.getdoc(func) or "")
    body = next(
        (doc.split(h, 1)[1] for h in ("Args:", "Arguments:", "Parameters") if h in doc),
        "",
    )
    import re

    pat = re.compile(r"^\s*(\w+)\s*:\s*(.+?)(?=\n\s*\w+\s*:|\Z)", re.S | re.M)
    return {n: " ".join(t.split()) for n, t in pat.findall(body)}


def _func_schema(func):
    props, required, docs = {}, [], _param_docs(func)
    for name, p in inspect.signature(func).parameters.items():
        if name in {"self", "cls"}:
            continue

        annot = p.annotation if p.annotation is not inspect._empty else str
        prop = _json_type(annot)

        if docs.get(name):
            prop["description"] = docs[name]
        props[name] = prop

        if p.default is inspect._empty:
            required.append(name)
    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def _type_schema(cls):
    props, required = {}, []
    for f in attrs.fields(cls):
        if f.name in _IGNORED:
            continue
        props[f.name] = _json_type(f.type) | {
            "description": f.metadata.get("description", f.name)
        }
        required.append(f.name)
    return {
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }


def serialize(self, obj: Any):
    if inspect.isfunction(obj):
        return {
            "type": "function",
            "name": obj.__name__,
            "description": (inspect.getdoc(obj) or "").split("\n")[0],
            "parameters": _func_schema(obj),
        }

    if inspect.isclass(obj):
        schema = _type_schema(obj) if attrs.has(obj) else {"type": "object"}
        return {
            "type": "json_schema",
            "name": obj.__name__,
            "schema": schema,
        }

    raise TypeError(f"Unsupported object: {obj!r}")


class Primitive(Enum):
    BOOLEAN = {"type": "number"}
    NUMBER = {"type": "integer"}
    FLOAT = {"type": "number"}
    STRING = {"type": "string"}
    LIST = {"type": "array", "items": {}}
    DICT = {"type": "object", "properties": {}}

    def __init__(self, primitive):
        self.primitive = primitive

    def __call__(self):
        return self.primitive

    @staticmethod
    def base():
        return {
            "type": "json_schema",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }

    @staticmethod
    def match(obj: Generic[T]):
        match type(obj):
            case bool():
                return Primitive.BOOLEAN
            case int():
                return Primitive.NUMBER
            case float():
                return Primitive.FLOAT
            case str():
                return Primitive.STRING
            case list():
                return Primitive.LIST
            case dict():
                return Primitive.DICT
