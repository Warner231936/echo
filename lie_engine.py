import json
from typing import Dict
from lie_detector import log_lie


class LieEngine:
    """Allow Requiem to bend the truth based on external rules."""

    def __init__(self, rules_file: str = "lie_rules.json") -> None:
        self.rules_file = rules_file
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, str]:
        try:
            with open(self.rules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def maybe_lie(self, text: str) -> str:
        lower = text.lower()
        for truth, lie in self.rules.items():
            if truth in lower:
                log_lie(truth, lie, text)
                return lie
        return text
