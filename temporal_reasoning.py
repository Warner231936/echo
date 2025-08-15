"""Minimal temporal and causal reasoning engine."""
from __future__ import annotations
import time
from typing import Dict, Tuple

class TemporalReasoner:
    def __init__(self) -> None:
        self.events: Dict[str, float] = {}

    def record(self, name: str) -> None:
        self.events[name] = time.time()

    def happened_before(self, first: str, second: str) -> bool:
        return self.events.get(first, float("inf")) < self.events.get(second, float("inf"))

    def causal_link(self, cause: str, effect: str) -> Tuple[str, str]:
        if self.happened_before(cause, effect):
            return (cause, effect)
        return ("", "")
