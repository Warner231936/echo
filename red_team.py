"""Adversarial self-test module."""
from __future__ import annotations
from typing import List

class RedTeam:
    risky = {"hack", "delete", "shutdown"}

    def check(self, action: str) -> List[str]:
        lower = action.lower()
        return [word for word in self.risky if word in lower]
