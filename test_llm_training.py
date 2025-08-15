import os
import shutil
import pytest

from llm.hf import HuggingFaceLLM

def test_alter_fine_tunes_and_saves():
    try:
        llm = HuggingFaceLLM("sshleifer/tiny-gpt2")
    except Exception:
        pytest.skip("local model not available")
    try:
        result = llm.alter("hello world")
        assert "fine-tuned" in result
        assert os.path.isdir("trained-model")
    finally:
        if os.path.isdir("trained-model"):
            shutil.rmtree("trained-model")
