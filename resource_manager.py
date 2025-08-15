"""Resource and energy management for Requiem."""
from __future__ import annotations

import time
from typing import Dict

try:  # pragma: no cover - psutil optional
    import psutil
except Exception:  # pragma: no cover
    psutil = None


class ResourceManager:
    def __init__(self, cpu_threshold: float = 90.0) -> None:
        self.cpu_threshold = cpu_threshold
        self.last_sample: Dict[str, float] = {}
        self.last_time = time.time()

    def sample(self) -> Dict[str, float]:
        cpu = psutil.cpu_percent() if psutil else 0.0
        mem = psutil.virtual_memory().percent if psutil else 0.0
        self.last_sample = {"cpu": cpu, "memory": mem}
        self.last_time = time.time()
        return self.last_sample

    def should_conserve(self) -> bool:
        """Whether to conserve energy based on recent sample."""
        cpu = self.last_sample.get("cpu", 0.0)
        return cpu > self.cpu_threshold
