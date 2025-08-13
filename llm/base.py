from abc import ABC, abstractmethod
from typing import Optional


class BaseLLM(ABC):
    """Abstract base class for language model clients."""

    @abstractmethod
    def reply(self, text: str, last_user: Optional[str]) -> str:
        """Return a reply from the model."""
        raise NotImplementedError
