from abc import ABC, abstractmethod
from typing import Optional


class BaseLLM(ABC):
    """Abstract base class for language model clients."""

    @abstractmethod
    def reply(self, text: str, last_user: Optional[str]) -> str:
        """Return a reply from the model."""
        raise NotImplementedError

    def alter(self, instructions: str) -> str:
        """Placeholder hook for self-modifying behavior."""
        return "model alteration not supported"
