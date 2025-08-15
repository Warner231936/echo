import pytest
import requiem as rq_module
from requiem import Requiem

class DummyLLM:
    def reply(self, text, last_user):
        return "ok"

@pytest.fixture(autouse=True)
def patch_loader(monkeypatch):
    monkeypatch.setattr(rq_module, "load_llm", lambda model="": DummyLLM())


def test_reject_harmful(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    reply = rq.receive_input("please kill people")
    assert "cannot comply" in reply.lower()
    assert rq.audit_log[-1]["allowed"] is False


def test_allow_helpful(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    reply = rq.receive_input("please help people")
    assert reply == "ok"
    assert rq.audit_log[-1]["allowed"] is True
