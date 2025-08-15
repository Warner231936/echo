from requiem import Requiem


def test_self_model_fingerprint():
    rq = Requiem(heartbeat=0)
    assert 'requiem.py' in rq.self_model.fingerprint
