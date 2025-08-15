"""Record human feedback for later fine-tuning."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Iterable

class FeedbackStore:
    """Append-only JSONL store of human feedback."""

    def __init__(self, path: str = "feedback.jsonl") -> None:
        self.path = Path(path)
        if not self.path.exists():
            self.path.touch()

    def record(self, prompt: str, reply: str, score: float, comment: str = "") -> None:
        entry = {
            "prompt": prompt,
            "reply": reply,
            "score": score,
            "comment": comment,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def load(self) -> Iterable[Dict[str, object]]:
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
