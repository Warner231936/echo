import sys
import importlib


def test_load_llm_fallback(monkeypatch):
    """load_llm returns an EchoLLM when no real models are available."""
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    monkeypatch.setitem(sys.modules, "llm.hf", None)
    import llm
    importlib.reload(llm)
    client = llm.load_llm("nonexistent-model")
    from llm import EchoLLM
    assert isinstance(client, EchoLLM)
    assert client.reply("hi", None).startswith("Echo:")
