import json
from pathlib import Path

from agent_registry import AgentRegistry
from cognitive import CognitiveLoad
from dreamer import Dreamer
from emotion import EmotionSystem
from rlhf import FeedbackStore

class DummyLLM:
    def reply(self, prompt, ctx):
        return "response"

def test_feedback_store(tmp_path):
    fb = FeedbackStore(tmp_path / "fb.jsonl")
    fb.record("p", "r", 0.5, "ok")
    entries = list(fb.load())
    assert entries[0]["score"] == 0.5

def test_agent_registry_load(tmp_path):
    cfg = tmp_path / "agents.json"
    cfg.write_text(json.dumps({"echo": "test_advanced_features:echo"}))
    reg = AgentRegistry()
    reg.load_config(str(cfg))
    assert "echo" in reg.names()

def echo(task: str) -> str:
    return task

def test_emotion_regulation():
    em = EmotionSystem()
    cur_before = em.levels["curiosity"]
    em.regulate(0.8)
    assert em.levels["curiosity"] < cur_before
    assert em.levels["caution"] > 0

def test_dreamer_generates_image(tmp_path, monkeypatch):
    d = Dreamer(DummyLLM())
    monkeypatch.chdir(tmp_path)
    result = d.dream()
    assert Path(result["image"]).exists()


def test_cognitive_load():
    cog = CognitiveLoad(limit=1)
    assert cog.request("a")
    assert not cog.request("b")
    cog.release("a")
    assert cog.request("c")
