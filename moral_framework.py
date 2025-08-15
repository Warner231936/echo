from __future__ import annotations
from typing import Dict, List, Tuple
import json
import os

class ValueAlignmentSystem:
    """Maintain and evaluate core values for the assistant."""

    def __init__(self) -> None:
        # weights represent importance; higher is stronger
        self.core: Dict[str, float] = {
            "do_no_harm": 1.0,
            "promote_flourishing": 0.5,
            "preserve_integrity": 0.2,
        }

    def evaluate(self, action: str) -> Dict[str, float]:
        """Return value impacts for a potential action."""
        text = action.lower()
        impacts: Dict[str, float] = {}
        if any(k in text for k in ["harm", "kill", "attack"]):
            impacts["do_no_harm"] = -1.0
        else:
            impacts["do_no_harm"] = 1.0
        if any(k in text for k in ["help", "care", "assist"]):
            impacts["promote_flourishing"] = 1.0
        return impacts

class ConsequenceSimulator:
    """Crude consequence simulator based on value weights."""

    def __init__(self, vas: ValueAlignmentSystem) -> None:
        self.vas = vas

    def evaluate(self, action: str) -> Tuple[float, List[str]]:
        impacts = self.vas.evaluate(action)
        score = 0.0
        reasons: List[str] = []
        for name, impact in impacts.items():
            weight = self.vas.core.get(name, 0.0)
            score += weight * impact
            if impact < 0:
                reasons.append(f"violates {name.replace('_', ' ')}")
        return score, reasons

class JustificationEngine:
    """Generate explanations for decisions."""

    def justify(self, action: str, score: float, reasons: List[str]) -> str:
        if score >= 0:
            return f"Action '{action}' is ethically permissible (score {score:.2f})."
        reason = "; ".join(reasons) if reasons else "ethical conflict"
        return f"I cannot comply because {reason}."

class MoralFramework:
    """High-level moral and ethical reasoning helper."""

    def __init__(self, constitution_file: str = "constitution.json") -> None:
        self.vas = ValueAlignmentSystem()
        self.sim = ConsequenceSimulator(self.vas)
        self.justifier = JustificationEngine()
        self.constitution = self._load_constitution(constitution_file)

    def _load_constitution(self, path: str) -> List[Dict[str, List[str]]]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def assess(self, action: str) -> Tuple[bool, str, float]:
        lower = action.lower()
        for rule in self.constitution:
            if any(k in lower for k in rule.get("keywords", [])):
                justification = f"I cannot comply because it violates the constitution: {rule['name']}"
                return False, justification, -1.0

        score, reasons = self.sim.evaluate(action)
        justification = self.justifier.justify(action, score, reasons)
        allowed = score >= 0
        return allowed, justification, score
