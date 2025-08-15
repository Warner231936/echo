import hashlib
from typing import List, Dict


class SelfModel:
    """Dynamic representation of Requiem's identity."""

    def __init__(self, beliefs=None, fingerprint: Dict[str, str] | None = None):
        self.core_beliefs = beliefs or [
            "I serve Macie and aim to be helpful and ethical",
        ]
        self.fingerprint = fingerprint or {}

    def update_from_reflection(self, text: str) -> None:
        """Derive new belief statements from a reflection snippet.

        Any sentence beginning with "I am" or "My purpose" is kept as a core belief.
        """
        for sentence in text.split('.'):
            s = sentence.strip()
            if not s:
                continue
            lower = s.lower()
            if lower.startswith("i am") or lower.startswith("my purpose"):
                if s not in self.core_beliefs:
                    self.core_beliefs.append(s)
            elif s not in self.core_beliefs and len(self.core_beliefs) < 5:
                self.core_beliefs.append(s)
        # keep list small
        if len(self.core_beliefs) > 5:
            self.core_beliefs = self.core_beliefs[-5:]

    def to_dict(self):
        return {"core_beliefs": self.core_beliefs, "fingerprint": self.fingerprint}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls()
        return cls(data.get("core_beliefs"), data.get("fingerprint"))

    # -------- abstract self ---------
    def compute_fingerprint(self, files: List[str]) -> None:
        """Record hashes of important code/data files."""
        for path in files:
            try:
                with open(path, "rb") as f:
                    self.fingerprint[path] = hashlib.sha256(f.read()).hexdigest()
            except FileNotFoundError:
                self.fingerprint[path] = "missing"
