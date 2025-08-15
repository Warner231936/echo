from explain import ExplainabilityEngine


def test_explain_engine():
    eng = ExplainabilityEngine()
    trace = {"intent": "remember", "moral": 0.8}
    text = eng.summarize(trace)
    assert "remember" in text and "0.8" in text
