"""Explainability and interpretability engine."""
from __future__ import annotations

from typing import Dict


class ExplainabilityEngine:
    def summarize(self, trace: Dict) -> str:
        intent = trace.get("intent", "unknown")
        moral = trace.get("moral")
        score = moral if isinstance(moral, (int, float)) else trace.get("moral", 0)
        return f"Handled intent '{intent}' with moral score {score}."
