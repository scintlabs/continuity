from __future__ import annotations

from typing import Any, Dict

from attrs import define, field


@define
class Repository:
    outlines: Dict[str, Any] = field(factory=dict)
    tools: Dict[str, Any] = field(factory=dict)

    # Outline CRUD methods
    def add_outline(self, name: str, outline: Any) -> None:
        """Store a new outline."""

        self.outlines[name] = outline

    def get_outline(self, name: str) -> Any | None:
        """Retrieve an outline by name."""

        return self.outlines.get(name)

    def update_outline(self, name: str, outline: Any) -> None:
        """Update or create an outline."""

        self.outlines[name] = outline

    def delete_outline(self, name: str) -> None:
        """Remove an outline if present."""

        self.outlines.pop(name, None)

    def list_outlines(self) -> list[str]:
        """Return the names of all stored outlines."""

        return list(self.outlines)

    # Tool CRUD methods
    def add_tool(self, name: str, tool: Any) -> None:
        """Store a new tool."""

        self.tools[name] = tool

    def get_tool(self, name: str) -> Any | None:
        """Retrieve a tool by name."""

        return self.tools.get(name)

    def update_tool(self, name: str, tool: Any) -> None:
        """Update or create a tool."""

        self.tools[name] = tool

    def delete_tool(self, name: str) -> None:
        """Remove a tool if present."""

        self.tools.pop(name, None)

    def list_tools(self) -> list[str]:
        """Return the names of all stored tools."""

        return list(self.tools)
