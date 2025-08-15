from self_improver import SelfImprover


def test_self_improver_suggests():
    si = SelfImprover()
    si.note_issue("test")
    assert si.review() == "Consider addressing: test"
