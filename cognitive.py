"""Simple cognitive load manager."""
from __future__ import annotations
from typing import Set

class CognitiveLoad:
    def __init__(self, limit: int = 3) -> None:
        self.limit = limit
        self.active: Set[str] = set()

    def request(self, name: str) -> bool:
        if len(self.active) >= self.limit:
            return False
        self.active.add(name)
        return True

    def release(self, name: str) -> None:
        self.active.discard(name)
