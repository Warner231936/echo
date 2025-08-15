from planner import ActionPlanner
from emotion import EmotionSystem


def test_planner_creates_actions():
    ap = ActionPlanner()
    ap.plan("learn quantum computing")
    assert ap.has_actions()
    first = ap.next_action()
    assert "search web" in first


def test_emotion_updates():
    es = EmotionSystem()
    es.update_from_trace(0.8)
    assert es.levels["joy"] > 0
    es.goal_feedback(1.0)
    assert es.levels["satisfaction"] > 0
