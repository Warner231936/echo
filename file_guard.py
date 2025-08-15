from typing import Iterable


class FileGuard:
    """Prevent access to sensitive files."""

    def __init__(self, blocked: Iterable[str] | None = None) -> None:
        self.blocked = set(blocked or [])

    def is_blocked(self, text: str) -> bool:
        return any(name in text for name in self.blocked)
