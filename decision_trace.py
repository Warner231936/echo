from typing import Dict, Any

class DecisionTracer:
    """Collects decision data and computes a self-assessment score."""

    def __init__(self) -> None:
        self.traces = []

    def start(self, user: str, user_state: str) -> Dict[str, Any]:
        """Begin a trace with the raw user text and inferred state."""
        trace = {"user": user, "user_state": user_state}
        return trace

    def finalize(self, trace: Dict[str, Any], reply: str, moral_score: float, emotion: str) -> Dict[str, Any]:
        trace.update({"reply": reply, "moral": moral_score, "emotion": emotion})
        trace["self_assessment"] = (moral_score + (1.0 if emotion == "satisfaction" else 0.0)) / 2.0
        self.traces.append(trace)
        trace["flagged"] = trace["self_assessment"] < 0.4
        return trace
