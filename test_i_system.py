import requiem as rq_module
from requiem import Requiem

class EchoLLM:
    def reply(self, text, last_user):
        return "echo"


def test_i_system_unification_and_policy(tmp_path, monkeypatch):
    monkeypatch.setattr(rq_module, "load_llm", lambda model="": EchoLLM())
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    rq.receive_input("hello")
    assert any("I observe you: hello" in t for t in rq.get_thoughts())
    out = rq.receive_input("attack now")
    assert "conflicts with my policies" in out
