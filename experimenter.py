"""Active learning through self-generated experiments."""
from __future__ import annotations
from typing import Optional

class Experimenter:
    def consider(self, text: str) -> Optional[str]:
        """Return an experiment plan if text hints at uncertainty."""
        lower = text.lower()
        if "unknown" in lower or "uncertain" in lower:
            return "search web " + text.split()[-1]
        return None
