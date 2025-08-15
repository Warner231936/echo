import os
import tempfile
from requiem import Requiem


def test_self_modification_requires_approval():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    def approve(action: str):
        return True
    rq = Requiem(heartbeat=0, approver=approve)
    rq.receive_input(f"self modify {tmp.name} hello")
    with open(tmp.name, "r", encoding="utf-8") as f:
        assert f.read() == "hello"
    os.unlink(tmp.name)


def test_run_code_needs_approval():
    called = {}
    def approve(action: str):
        called['a'] = action
        return True
    rq = Requiem(heartbeat=0, approver=approve)
    out = rq.receive_input("run code print('x')")
    assert "x" in out
    assert called['a'] == 'run_code'
