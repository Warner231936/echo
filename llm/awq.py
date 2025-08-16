from typing import Optional

from .base import BaseLLM


class AWQLLM(BaseLLM):
    """Quantized AWQ chat model running on GPU when available."""

    def __init__(self, model: str) -> None:
        import torch
        from transformers import AutoTokenizer, TextStreamer
        from awq import AutoAWQForCausalLM

        self.tokenizer = AutoTokenizer.from_pretrained(model, use_fast=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"

        self.model = AutoAWQForCausalLM.from_quantized(
            model,
            device_map="auto",
            fuse_layers=True,
        )
        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        self.gen_cfg = {
            "max_new_tokens": 256,
            "do_sample": True,
            "temperature": 0.8,
            "top_p": 0.9,
            "repetition_penalty": 1.15,
            "eos_token_id": self.tokenizer.eos_token_id,
            "pad_token_id": self.tokenizer.pad_token_id,
        }

    def reply(self, text: str, last_user: Optional[str]) -> str:
        import torch

        messages = [
            {"role": "system", "content": "You are Requiem: concise, concrete, no pep-talk filler."},
            {"role": "user", "content": text.strip()},
        ]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        enc = self.tokenizer(prompt, return_tensors="pt", padding=True).to(self.model.device)
        with torch.no_grad():
            out = self.model.generate(
                **enc,
                attention_mask=enc["attention_mask"],
                **self.gen_cfg,
            )
        return self.tokenizer.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)

    def alter(self, instructions: str) -> str:
        return f"awq model noted: {instructions}"
