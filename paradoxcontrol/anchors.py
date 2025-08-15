from dataclasses import dataclass, field
from typing import List, Dict, Set

@dataclass
class Anchor:
    id: str
    name: str
    summary: str
    frames_on: List[str] = field(default_factory=list)
    frame_weights: Dict[str, float] = field(default_factory=dict)
    hard_triggers: List[str] = field(default_factory=list)
    soft_triggers: List[str] = field(default_factory=list)
    priority: float = 0.5
    use_count: int = 0

@dataclass
class AnchorSet:
    anchors: Dict[str, Anchor] = field(default_factory=dict)

    def add(self, a: Anchor): self.anchors[a.id] = a
    def get(self, aid: str) -> Anchor: return self.anchors[aid]

    def active_frames(self, active_ids: List[str]) -> Set[str]:
        frames = set()
        for aid in active_ids:
            a = self.anchors.get(aid); 
            if a: frames.update(a.frames_on)
        return frames

    def weights_for(self, active_ids: List[str]) -> Dict[str, float]:
        w = {}
        for aid in active_ids:
            a = self.anchors.get(aid)
            if not a: continue
            for f, mul in (a.frame_weights or {}).items():
                w[f] = max(w.get(f, 1.0), mul)
        return w
