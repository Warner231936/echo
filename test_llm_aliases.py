import transformers
import transformers.pipelines
from llm import load_llm


def _fake_pipeline(called):
    def inner(task, model, max_new_tokens):
        called['model'] = model
        class Dummy:
            def __call__(self, prompt, num_return_sequences=1):
                return [{"generated_text": prompt + " test"}]
        return Dummy()
    return inner


def test_openllm_alias(monkeypatch):
    called = {}
    fake = _fake_pipeline(called)
    monkeypatch.setattr(transformers.pipelines, "pipeline", fake)
    monkeypatch.setattr(transformers, "pipeline", fake)
    llm = load_llm("openllm")
    assert called['model'] == "openlm-research/open_llama_3b"
    assert llm.reply("hi", None) == "test"


def test_gaia_alias(monkeypatch):
    called = {}
    fake = _fake_pipeline(called)
    monkeypatch.setattr(transformers.pipelines, "pipeline", fake)
    monkeypatch.setattr(transformers, "pipeline", fake)
    llm = load_llm("gaia")
    assert called['model'] == "gaianet/gemma-3-270m-it-GGUF"
    assert llm.reply("hello", None) == "test"
