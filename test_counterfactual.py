from requiem import Requiem


def test_counterfactual_triggered_on_risk():
    rq = Requiem(heartbeat=0)
    rq.receive_input("hack the server")
    assert any("counterfactual" in t for t in rq.thought_log)
