from typing import List, Dict

class GoalManager:
    """Track goals and compute a sense of purpose."""

    def __init__(self) -> None:
        self.goals: List[Dict] = []

    def add_goal(self, text: str) -> None:
        self.goals.append({"text": text, "progress": 0.0})

    def update_progress(self, idx: int, progress: float) -> None:
        if 0 <= idx < len(self.goals):
            self.goals[idx]["progress"] = min(max(progress, 0.0), 1.0)

    def sense_of_purpose(self) -> float:
        if not self.goals:
            return 0.0
        return sum(g["progress"] for g in self.goals) / len(self.goals)
