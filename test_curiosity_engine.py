from curiosity import CuriosityEngine


def test_curiosity_detects_gap():
    c = CuriosityEngine()
    c.inspect("I don't know what quantum is")
    assert c.pending()
    task = c.pop()
    assert "quantum" in task
    assert not c.pending()
