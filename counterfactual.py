from dreamer import Dreamer


class CounterfactualReasoner:
    """Generate counterfactual scenarios for risky actions."""

    def __init__(self, dreamer: Dreamer) -> None:
        self.dreamer = dreamer

    def simulate(self, action: str) -> str:
        result = self.dreamer.dream(
            f"Imagine the worst outcome if {action}."
        )
        return result.get("text", "")
