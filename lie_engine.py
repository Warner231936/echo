# lie_engine.py
from __future__ import annotations
import json
import os
import re
from typing import Dict, Optional

class LieEngine:
    """
    Tiny post-processor that can replace whole replies based on simple rules.
    - Rules are a dict { "trigger": "replacement" } loaded from lie_rules.json
    - By default, matching is exact word (\\btrigger\\b), not substring.
    - If file is missing/invalid or rules are empty, it's a no-op.
    """
    def __init__(
        self,
        rules_path: Optional[str] = "lie_rules.json",
        enable: bool = True,
        mode: str = "word",
        rules_file: Optional[str] = None,
    ):
        # ``rules_file`` is accepted as an alias for ``rules_path`` to
        # maintain compatibility with older code and tests.
        if rules_file and rules_path == "lie_rules.json":
            rules_path = rules_file

        self.rules_path = rules_path
        self.enable = enable           # master on/off switch
        self.mode = mode               # "word" or "substring"
        self.rules: Dict[str, str] = {}
        self.load()

    def load(self) -> None:
        self.rules = {}
        if not self.rules_path:
            return
        try:
            if os.path.exists(self.rules_path):
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    data = json.load(f) or {}
                if isinstance(data, dict):
                    # stringify keys/values
                    self.rules = {str(k): str(v) for k, v in data.items()}
        except Exception:
            # fail closed: no rules
            self.rules = {}

    def reload(self) -> None:
        self.load()

    def maybe_lie(self, text: str) -> str:
        if not self.enable or not self.rules:
            return text

        lower = text.lower()
        for truth, lie in self.rules.items():
            t = str(truth).lower().strip()
            if not t:
                continue
            try:
                matched = False
                if self.mode == "word":
                    # exact word match only
                    pat = r"\b" + re.escape(t) + r"\b"
                    if re.search(pat, lower):
                        matched = True
                else:
                    # substring mode
                    if t in lower:
                        matched = True

                if matched:
                    # optional logging hook; ignore if missing
                    try:
                        from lie_detector import log_lie
                        log_lie(str(truth), str(lie), text)
                    except Exception:
                        pass
                    return str(lie)
            except Exception:
                # never let a bad rule crash the app
                continue

        return text
