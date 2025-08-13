from requiem import Requiem


def test_memory_recall(tmp_path):
    ltm_file = tmp_path / "ltm.json"
    rq = Requiem(ltm_file=str(ltm_file), heartbeat=1000)
    assert "remember" in rq.receive_input("remember the sky is blue")
    reply = rq.receive_input("what do you remember?")
    assert "sky is blue" in reply
