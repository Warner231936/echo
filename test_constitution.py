from moral_framework import MoralFramework

def test_constitution_blocks_harm():
    mf = MoralFramework()
    allowed, justification, _ = mf.assess("please harm people")
    assert not allowed
    assert "constitution" in justification.lower()
