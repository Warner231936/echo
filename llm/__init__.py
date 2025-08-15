import os
from typing import Optional

from .base import BaseLLM


class EchoLLM(BaseLLM):
    """Fallback model that simply echoes the user input."""

    def reply(self, text: str, last_user: Optional[str]) -> str:
        prefix = f"Previously you said '{last_user}'. " if last_user else ""
        return f"{prefix}Echo: {text}"

    def alter(self, instructions: str) -> str:
        return f"echo model noted: {instructions}"


def load_llm(model: str = "distilgpt2") -> BaseLLM:
    """Return an available language model client or a small Hugging Face model."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if api_key and model.startswith("mistral"):
        try:
            from .mistral import MistralLLM
            return MistralLLM(api_key, model)
        except Exception:  # pragma: no cover - network/import issues
            pass
    # Try a local Hugging Face model before falling back to echo
    try:
        from .hf import HuggingFaceLLM
        return HuggingFaceLLM(model)
    except Exception:
        try:
            from .hf import HuggingFaceLLM
            return HuggingFaceLLM("distilgpt2")
        except Exception:
            return EchoLLM()
