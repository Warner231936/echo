"""Simple recursive self-improvement tracker."""
from __future__ import annotations

from typing import List, Optional


class SelfImprover:
    """Collects issues and suggests fixes using internal reflection."""

    def __init__(self) -> None:
        self.issues: List[str] = []
        self.suggestions: List[str] = []

    def note_issue(self, description: str) -> None:
        self.issues.append(description)

    def review(self) -> Optional[str]:
        """Return a suggestion if any issues are pending."""
        if not self.issues:
            return None
        issue = self.issues.pop(0)
        suggestion = f"Consider addressing: {issue}"
        self.suggestions.append(suggestion)
        return suggestion
