import os
from typing import Optional, List

from .base import BaseLLM


class EchoLLM(BaseLLM):
    """Fallback model that simply echoes the user input."""

    def reply(self, text: str, last_user: Optional[str]) -> str:
        prefix = f"Previously you said '{last_user}'. " if last_user else ""
        return f"{prefix}Echo: {text}"

    def alter(self, instructions: str) -> str:
        return f"echo model noted: {instructions}"


def _candidate_models(preferred: Optional[str]) -> List[str]:
    """Return a list of models to try in order of preference."""
    candidates = []
    if preferred:
        candidates.append(preferred)
    env_model = os.environ.get("LLM_MODEL")
    if env_model:
        candidates.append(env_model)
    # include common small models as fallbacks
    candidates.extend(["distilgpt2", "sshleifer/tiny-gpt2"])
    seen = set()
    return [m for m in candidates if not (m in seen or seen.add(m))]


def load_llm(model: str = "distilgpt2") -> BaseLLM:
    """Return a local language model client, falling back to echo if unavailable."""

    models = _candidate_models(model)
    try:
        from .hf import HuggingFaceLLM
        for name in models:
            try:
                return HuggingFaceLLM(name)
            except Exception:
                continue
    except Exception:
        pass

    return EchoLLM()
