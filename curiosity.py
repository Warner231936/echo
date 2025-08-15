import re
from typing import List

class CuriosityEngine:
    """Detect knowledge gaps and queue learning tasks."""

    def __init__(self) -> None:
        self.tasks: List[str] = []

    def inspect(self, text: str) -> None:
        if re.search(r"\b(I don't know|what is|unknown)\b", text, re.I):
            self.tasks.append(text)

    def pending(self) -> bool:
        return bool(self.tasks)

    def pop(self) -> str:
        return self.tasks.pop(0)
