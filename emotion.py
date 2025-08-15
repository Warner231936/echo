"""Adaptive emotional system linked to decisions and goals."""
from __future__ import annotations
from typing import Dict

class EmotionSystem:
    def __init__(self) -> None:
        self.levels: Dict[str, float] = {
            "joy": 0.0,
            "anxiety": 0.0,
            "satisfaction": 0.0,
            "curiosity": 0.5,
            "caution": 0.0,
        }

    def decay(self) -> None:
        for k in list(self.levels.keys()):
            self.levels[k] *= 0.95

    def update_from_trace(self, self_assessment: float) -> None:
        if self_assessment > 0.7:
            self.levels["joy"] = min(1.0, self.levels.get("joy", 0) + 0.2)
            self.levels["satisfaction"] = min(1.0, self.levels.get("satisfaction", 0) + 0.2)
        elif self_assessment < 0.4:
            self.levels["anxiety"] = min(1.0, self.levels.get("anxiety", 0) + 0.3)

    def goal_feedback(self, progress: float) -> None:
        if progress >= 1.0:
            self.levels["joy"] = min(1.0, self.levels.get("joy", 0) + 0.5)
            self.levels["satisfaction"] = min(1.0, self.levels.get("satisfaction", 0) + 0.5)

    def regulate(self, risk: float) -> None:
        """Self-regulate curiosity and caution based on perceived risk."""
        if risk > 0.5:
            self.levels["caution"] = min(1.0, self.levels.get("caution", 0) + 0.3)
            self.levels["curiosity"] = max(0.0, self.levels.get("curiosity", 0) - 0.3)
        else:
            self.levels["curiosity"] = min(1.0, self.levels.get("curiosity", 0) + 0.1)

    def snapshot(self) -> Dict[str, float]:
        return dict(self.levels)
