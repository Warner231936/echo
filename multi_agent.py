"""Task delegation among multiple simple agents."""
from __future__ import annotations
from typing import Callable, Any
from agent_registry import AgentRegistry


class TaskDelegator:
    """Forward tasks to agents discovered via a registry."""

    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or AgentRegistry()

    def register(self, name: str, handler: Callable[[str], Any]) -> None:
        self.registry.register(name, handler)

    def delegate(self, name: str, task: str) -> Any:
        agent = self.registry.get(name)
        if not agent:
            raise KeyError(f"unknown agent {name}")
        return agent(task)
