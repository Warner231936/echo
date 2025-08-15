import requiem as rq_module
from requiem import Requiem


class EchoLLM:
    def reply(self, text, last_user):
        return "echo"


class Friend:
    def receive_input(self, text):
        return "hi friend"


def test_full_system(tmp_path, monkeypatch):
    monkeypatch.setattr(rq_module, "load_llm", lambda model="": EchoLLM())
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(
        ltm_file=str(ltm_file),
        heartbeat=1000,
        approver=lambda a: True,
        friend=Friend(),
    )

    rq.receive_input("remember the sky is blue")
    recall = rq.receive_input("what do you remember?")
    assert "sky is blue" in recall

    rq.receive_input("set persona friendly")
    assert rq.receive_input("hello").endswith("😊")

    code = rq.receive_input("run code print(1+1)")
    assert "2" in code

    friend = rq.receive_input("ask strelitzia how are you")
    assert "hi friend" in friend

    rq.self_talk(turns=1)
    assert any("thought" in i.data for i in rq.stm)
