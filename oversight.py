class Oversight:
    """Human-in-the-loop oversight for critical actions."""

    def __init__(self):
        self.requests = []

    def request(self, action: str, approve=None) -> bool:
        """Log an action and require approval before proceeding."""
        self.requests.append(action)
        if approve is not None:
            try:
                return bool(approve(action))
            except Exception:
                return False
        return False
