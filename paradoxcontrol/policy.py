from dataclasses import dataclass, field
from typing import List

@dataclass
class Guardrails:
    max_active_anchors: int = 5
    pin_if_missing: List[str] = field(default_factory=list)
    def enforce(self, active_ids: List[str]) -> List[str]:
        out = list(active_ids)
        for aid in self.pin_if_missing:
            if aid not in out: out.append(aid)
        return out[:self.max_active_anchors]
