"""Minimal theory-of-mind heuristics."""

from typing import Literal

class TheoryOfMind:
    """Infer coarse user emotion from text."""

    def infer(self, text: str) -> Literal["happy", "sad", "angry", "neutral"]:
        t = text.lower()
        if any(k in t for k in ["happy", "glad", "thanks"]):
            return "happy"
        if any(k in t for k in ["sad", "unhappy", "depressed"]):
            return "sad"
        if any(k in t for k in ["angry", "mad"]):
            return "angry"
        return "neutral"
