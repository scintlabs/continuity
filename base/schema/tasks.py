from __future__ import annotations

from typing import Any, Dict, List

from attrs import define, field

from base.schema.messages import Content, Instructions


@define
class ToolCall:
    call_id: str = field(default=None)
    tool_name: str = field(factory=str)
    arguments: Dict[str, Any] = field(factory=dict)


@define
class ToolResult:
    call_id = field(default=None)
    tool_name: str = field(factory=str)
    content: Content = field(factory=str)


@define
class Task:
    id: str = field(default=None)
    instructions: Instructions = field(default=None)


@define
class TaskResult:
    task_id: str = field()
    content: Content = field()


@define
class Process:
    id: str = field(default=None)
    results: ProcessResult = field(default=None)


@define
class ProcessResult:
    process_id: str = field()
    task_results: List[TaskResult] = field(factory=list)
