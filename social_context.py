"""Dynamic social and cultural context tracking for Requiem."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Profile:
    """Represents conversational knowledge about an agent."""
    name: str
    interactions: int = 0
    style: str = "casual"  # could be 'formal', 'friendly', etc.
    history: List[str] = field(default_factory=list)

    def update(self, message: str) -> None:
        self.interactions += 1
        self.history.append(message)
        # naive style inference
        if self.name.lower() == "macie":
            self.style = "formal"
        elif self.interactions > 5:
            self.style = "friendly"


class SocialContext:
    """Tracks conversation history and inferred relationships."""

    def __init__(self) -> None:
        self.profiles: Dict[str, Profile] = {}
        self.history: List[Tuple[str, str]] = []  # (speaker, message)

    def record(self, speaker: str, message: str) -> None:
        profile = self.profiles.setdefault(speaker, Profile(speaker))
        profile.update(message)
        self.history.append((speaker, message))

    def style_for(self, speaker: str) -> str:
        return self.profiles.get(speaker, Profile(speaker)).style

    def relationship(self, speaker: str) -> Profile:
        return self.profiles.get(speaker, Profile(speaker))
