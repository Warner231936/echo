"""Interfaces for pluggable language model clients."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseLLM(ABC):
    """Abstract base class for language model clients."""

    name: str = "base"

    @abstractmethod
    def reply(self, text: str, last_user: Optional[str]) -> str:
        """Return a reply from the model."""
        raise NotImplementedError

    def alter(self, instructions: str) -> str:
        """Alter the underlying model (e.g., a light fine‑tune).

        Subclasses may override to perform local training steps that adapt the
        model to the provided instructions. The default implementation indicates
        that alteration is unsupported.
        """
        raise NotImplementedError("model alteration not supported")
