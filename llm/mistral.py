from typing import Optional

from .base import BaseLLM

try:  # pragma: no cover - optional dependency
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
except ImportError:  # pragma: no cover
    MistralClient = None
    ChatMessage = None


class MistralLLM(BaseLLM):
    """Wrapper around the Mistral chat API."""

    def __init__(self, api_key: str, model: str) -> None:
        if MistralClient is None:
            raise RuntimeError("mistralai package is required for MistralLLM")
        self.client = MistralClient(api_key)
        self.model = model

    def reply(self, text: str, last_user: Optional[str]) -> str:
        messages = [ChatMessage(role="system", content="You are Requiem, a helpful assistant.")]
        if last_user:
            messages.append(ChatMessage(role="assistant", content=last_user))
        messages.append(ChatMessage(role="user", content=text))
        resp = self.client.chat(model=self.model, messages=messages)
        return resp.choices[0].message.content
