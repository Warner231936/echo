from .base import BaseLLM

class HuggingFaceLLM(BaseLLM):
    """Lightweight wrapper around a small Hugging Face model."""

    def __init__(self, model: str = "distilgpt2") -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # lazy import

        # load tokenizer and model locally; will raise if files are missing
        tok = AutoTokenizer.from_pretrained(model, local_files_only=True)
        mdl = AutoModelForCausalLM.from_pretrained(model, local_files_only=True)
        self.pipe = pipeline("text-generation", model=mdl, tokenizer=tok, max_new_tokens=50)

    def reply(self, text: str, last_user):
        prompt = text
        out = self.pipe(prompt, num_return_sequences=1)[0]["generated_text"]
        return out[len(prompt):].strip()

    def alter(self, instructions: str) -> str:
        """Perform a tiny fine‑tuning step on the local model."""
        import torch

        model = self.pipe.model
        tokenizer = self.pipe.tokenizer
        model.train()
        inputs = tokenizer(instructions, return_tensors="pt")
        labels = inputs["input_ids"].clone()
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        model.eval()
        save_dir = "trained-model"
        model.save_pretrained(save_dir)
        tokenizer.save_pretrained(save_dir)
        return f"fine-tuned ({loss.item():.4f})"
