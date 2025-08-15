from multi_agent import TaskDelegator
from temporal_reasoning import TemporalReasoner
from experimenter import Experimenter
from dreamer import Dreamer
from red_team import RedTeam

class DummyLLM:
    def reply(self, prompt, _):
        return "dreamed"

def test_task_delegation():
    mgr = TaskDelegator()
    mgr.register("echo", lambda t: t.upper())
    assert mgr.delegate("echo", "hi") == "HI"

def test_temporal_reasoner():
    tr = TemporalReasoner()
    tr.record("a")
    tr.record("b")
    assert tr.happened_before("a", "b")

def test_experimenter_and_redteam_and_dreamer():
    exp = Experimenter()
    assert exp.consider("this is unknown territory").startswith("search web")
    rt = RedTeam()
    assert rt.check("please hack system") == ["hack"]
    dr = Dreamer(DummyLLM())
    dream = dr.dream()
    assert dream["text"] == "dreamed"
    assert "image" in dream
