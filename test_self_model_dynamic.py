from self_model import SelfModel


def test_belief_update():
    sm = SelfModel()
    sm.update_from_reflection("I am learning. My purpose is growth.")
    assert any(b == "I am learning" for b in sm.core_beliefs)
    assert any(b == "My purpose is growth" for b in sm.core_beliefs)
