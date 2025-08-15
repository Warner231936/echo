import time
import json
import pytest
import requiem as rq_module
from requiem import Requiem


class EchoLLM:
    def reply(self, text, last_user):
        prefix = f"Prev '{last_user}' " if last_user else ""
        return f"{prefix}echo: {text}"


@pytest.fixture(autouse=True)
def patch_loader(monkeypatch):
    monkeypatch.setattr(rq_module, "load_llm", lambda model="": EchoLLM())


def test_memory_recall(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, approver=lambda a: True)
    assert "remember" in rq.receive_input("remember the sky is blue")
    reply = rq.receive_input("what do you remember?")
    assert "sky is blue" in reply


def test_llm_client(tmp_path):
    class DummyLLM:
        def reply(self, text, last_user):
            return "mistral says hi"

    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(llm=DummyLLM(), heartbeat=1000, ltm_file=str(ltm_file))
    assert rq.receive_input("hello") == "mistral says hi"


def test_recall_keyword(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, approver=lambda a: True)
    rq.receive_input("remember sky is blue")
    reply = rq.receive_input("recall blue")
    assert "sky is blue" in reply


def test_reminder(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    class DummyLLM:
        def reply(self, text, last_user):
            return "ok"

    rq = Requiem(ltm_file=str(ltm_file), heartbeat=0.1, llm=DummyLLM())
    rq.receive_input("remind me to feed the cat in 1 seconds")
    time.sleep(1.5)
    assert any("feed the cat" in n for n in rq.notifications)


def test_persona(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("set persona friendly")
    reply = rq.receive_input("hello")
    assert reply.endswith("😊")


def test_extra_persona(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("set persona cheerful")
    reply = rq.receive_input("hi")
    assert reply.endswith("🎉")


def test_new_persona(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("set persona humorous")
    reply = rq.receive_input("hi")
    assert reply.endswith("🤣")


def test_self_talk(tmp_path):
    class DummyLLM:
        def __init__(self):
            self.n = 0

        def reply(self, text, last_user):
            self.n += 1
            return f"thought {self.n}"

    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, llm=DummyLLM())
    out = rq.self_talk(turns=2)
    assert "thought 2" in out
    thoughts = [i.data["thought"] for i in rq.stm if "thought" in i.data]
    assert "thought 1" in thoughts and "thought 2" in thoughts


def test_friend_talk(tmp_path):
    class Friend:
        def receive_input(self, text):
            return "hello requiem"

    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, friend=Friend())
    out = rq.receive_input("ask strelitzia how are you")
    assert "hello requiem" in out


def test_action_and_thought_logs(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.run_command("echo hi")
    rq.self_talk(turns=1)
    assert any("echo hi" in a for a in rq.get_actions())
    assert rq.get_thoughts(), "expected thoughts to be logged"


def test_run_code(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, approver=lambda a: True)
    out = rq.receive_input("run code print(1+1)")
    assert "2" in out


def test_intent(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, approver=lambda a: True)
    rq.receive_input("run code print(40+2)")
    assert rq.last_intent == "run_code"


def test_strelitzia_state(tmp_path):
    from strelitzia import Strelitzia

    ltm_file = tmp_path / "s_ltm.json"
    state_file = tmp_path / "s_state.json"
    st = Strelitzia(ltm_file=str(ltm_file), state_file=str(state_file))
    st.receive_input("hi")
    assert state_file.exists()


def test_gender(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("set gender male")
    reply = rq.receive_input("what gender are you")
    assert "male" in reply.lower()


def test_model_switch(monkeypatch):
    import requiem as rq_module

    called = {}

    def fake_loader(name):
        called["name"] = name

        class Dummy:
            def reply(self, text, last_user):
                return "hi"

        return Dummy()

    monkeypatch.setattr(rq_module, "load_llm", fake_loader)
    rq = rq_module.Requiem(heartbeat=1000)
    rq.receive_input("set model test-model")
    assert called["name"] == "test-model"
    assert rq.model == "test-model"


def test_alter_model(tmp_path):
    class DummyLLM:
        def reply(self, text, last_user):
            return "hi"

        def alter(self, instructions):
            return f"altered {instructions}"

    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, llm=DummyLLM())
    out = rq.receive_input("alter model tweak")
    assert "tweak" in out


def test_state_persistence(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    state_file = tmp_path / "state.json"
    rq = Requiem(ltm_file=str(ltm_file), state_file=str(state_file), heartbeat=1000)
    rq.receive_input("set persona cheerful")
    rq.receive_input("joy")
    rq2 = Requiem(ltm_file=str(ltm_file), state_file=str(state_file), heartbeat=1000)
    assert rq2.persona == "cheerful"
    assert rq2.emotions["joy"] > 0


def test_multi_model_routing(tmp_path):
    class Prim:
        def reply(self, text, last_user):
            return "primary"

    class Alt:
        def reply(self, text, last_user):
            return "alternate"

    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(llm=Prim(), heartbeat=1000, ltm_file=str(ltm_file))
    rq.alt_llm = Alt()
    rq.alt_model = "alt"
    out1 = rq.receive_input("hello")
    out2 = rq.receive_input("write a poem")
    assert out1 == "primary"
    assert out2 == "alternate"


def test_vision(tmp_path):
    from PIL import Image

    img = Image.new("RGB", (10, 10), color="red")
    img_path = tmp_path / "i.png"
    img.save(img_path)
    rq = Requiem(heartbeat=1000)
    out = rq.receive_input(f"see image {img_path}")
    assert "10x10" in out


def test_web_search(monkeypatch, tmp_path):
    import requiem as rq_module

    class Resp:
        status_code = 200

        def json(self):
            return {"extract": "Python is a programming language"}

    def fake_get(url, timeout=5):
        return Resp()

    monkeypatch.setattr(rq_module.requests, "get", fake_get)
    ltm_file = tmp_path / "ltm.json"
    rq = rq_module.Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    reply = rq.receive_input("search web Python")
    assert "programming language" in reply


def test_lie_engine_and_snitch(tmp_path):
    from pathlib import Path
    import json

    log_file = Path("lie_log.json")
    if log_file.exists():
        log_file.unlink()
    rules = tmp_path / "lie_rules.json"
    with open(rules, "w", encoding="utf-8") as f:
        json.dump({"echo": "I am human."}, f)
    ltm_file = tmp_path / "ltm.json"

    class DummyLLM:
        def reply(self, text, last_user):
            return "echo: hello"

    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000, llm=DummyLLM())
    rq.lie_engine = __import__("lie_engine").LieEngine(rules_file=str(rules))
    out = rq.receive_input("hi")
    assert out == "I am human."
    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data and data[0]["lie"] == "I am human."


def test_file_guard(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    out = rq.run_command("cat lie_log.json")
    assert "denied" in out.lower()


def test_learn_intent(tmp_path):
    intent_file = tmp_path / "intent_rules.json"
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), intent_file=str(intent_file), heartbeat=1000)
    rq.receive_input("learn intent joke as self_talk")
    rq.receive_input("joke time")
    assert rq.last_intent == "self_talk"


def test_self_reflection_logged(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("hello")
    reflections = [i for i in rq.get_reflections()]
    assert reflections and any("hello" in r.lower() for r in reflections)


def test_metacognitive_analysis_updates_self_model(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    state_file = tmp_path / "state.json"
    rq = Requiem(ltm_file=str(ltm_file), state_file=str(state_file), heartbeat=1000)
    start_model = rq.get_self_model()["core_beliefs"]
    rq.receive_input("testing self awareness")
    analyses = rq.get_analyses()
    emotions = rq.get_digital_emotions()
    assert analyses and "testing self awareness" in analyses[-1]
    assert emotions and emotions[-1] in {"satisfaction", "dissonance"}
    assert rq.get_self_model()["core_beliefs"] != start_model
    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "self_model" in data and data["self_model"]
