"""Record reflections as seed data for future self-improvement."""

class ReflectionTrainer:
    """Append reflections to a training data file."""

    def __init__(self, path: str = "reflections_train.txt") -> None:
        self.path = path

    def record(self, text: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(text.strip() + "\n")
