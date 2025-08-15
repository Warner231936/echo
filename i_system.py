import time
from typing import Any

class ISystem:
    """Coordinator that unifies perception, intent, and reflection."""

    def __init__(self, core: Any) -> None:
        self.core = core

    def unification(self) -> str:
        """Synthesize a narrative from recent interaction and emotion."""
        last = self.core.chat_log[-1] if self.core.chat_log else ""
        dominant = max(self.core.emotions, key=self.core.emotions.get) if self.core.emotions else "neutral"
        narrative = f"I observe {last} and feel {dominant}."
        self.core.thought_log.append(narrative)
        return narrative

    def agent_of_intent(self, text: str) -> str:
        """Classify text and enforce core policy."""
        intent = self.core.intent.classify(text)
        if not self.core.policy.allowed(text):
            return "reject"
        return intent

    def reflect(self, intent: str) -> None:
        """Record a reflection on the chosen intent."""
        entry = f"I decided on '{intent}'."
        self.core.reflection_log.append(entry)
        self.core.thought_log.append(f"reflection: {entry}")

    def process(self, text: str) -> str:
        """Run unification, intent analysis, and reflection."""
        self.unification()
        intent = self.agent_of_intent(text)
        self.reflect(intent)
        return intent
