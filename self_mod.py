from typing import Optional
from oversight import Oversight


class SelfModifier:
    """Allow Requiem to apply code changes with explicit approval."""

    def __init__(self, oversight: Oversight):
        self.oversight = oversight

    def modify(self, path: str, content: str, approve: Optional[callable] = None) -> bool:
        """Write content to path if oversight approves."""
        if not self.oversight.request(f"modify:{path}", approve):
            return False
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
