"""Proactive action planning engine for Requiem."""
from __future__ import annotations
from typing import List

class ActionPlanner:
    def __init__(self) -> None:
        self.queue: List[str] = []

    def plan(self, goal_text: str) -> None:
        gt = goal_text.lower()
        steps: List[str] = []
        if "learn" in gt or "improve" in gt:
            topic = goal_text.split(" ", 1)[-1]
            steps.append(f"search web {topic}")
            steps.append(f"remember summary of {topic}")
        elif "write" in gt:
            steps.append(f"run code print('draft {goal_text}')")
        for s in steps:
            self.queue.append(s)

    def has_actions(self) -> bool:
        return bool(self.queue)

    def next_action(self) -> str:
        return self.queue.pop(0)
