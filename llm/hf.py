from .base import BaseLLM

class HuggingFaceLLM(BaseLLM):
    """Lightweight wrapper around a small Hugging Face model."""

    def __init__(self, model: str = "distilgpt2") -> None:
        from transformers import pipeline  # lazy import

        self.pipe = pipeline("text-generation", model=model, max_new_tokens=50)
        # Explicitly set pad token to suppress transformers warning
        if self.pipe.model.config.pad_token_id is None:
            self.pipe.model.config.pad_token_id = self.pipe.tokenizer.eos_token_id
            self.pipe.tokenizer.pad_token_id = self.pipe.model.config.pad_token_id

    def reply(self, text: str, last_user):
        prompt = text
        out = self.pipe(prompt, num_return_sequences=1)[0]["generated_text"]
        return out[len(prompt):].strip()

    def alter(self, instructions: str) -> str:
        return f"hf model pending alteration: {instructions}"
