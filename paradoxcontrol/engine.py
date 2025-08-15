from dataclasses import dataclass, field
from typing import Dict, List
from .lattice import TV, tv_from_sc
from .anchors import AnchorSet

@dataclass
class Evidence:
    frame: str
    weight: float
    polarity: int  # +1 support, -1 counter
    source: str = ""

@dataclass
class Node:
    id: str
    text: str
    value: TV = TV.N
    evidence: List[Evidence] = field(default_factory=list)

@dataclass
class Graph:
    nodes: Dict[str, Node] = field(default_factory=dict)
    def add_node(self, node: Node): self.nodes[node.id] = node
    def add_evidence(self, node_id: str, ev: Evidence): self.nodes[node_id].evidence.append(ev)

@dataclass
class FixpointConfig:
    max_iters: int = 12
    tol_changes: int = 0
    verbose: bool = False

class Evaluator:
    def __init__(self, graph: Graph, anchors: AnchorSet):
        self.g = graph; self.anchors = anchors

    def _infer_node(self, node: Node, frames, weights) -> TV:
        s = c = 0.0
        for ev in node.evidence:
            if ev.frame not in frames: 
                continue
            w = ev.weight * weights.get(ev.frame, 1.0)
            if ev.polarity >= 0: s += w
            else:                c += w
        return tv_from_sc(s, c)

    def _step(self, frames, weights) -> int:
        changed = 0; new = {}
        for nid, node in self.g.nodes.items():
            new[nid] = self._infer_node(node, frames, weights)
        for nid, val in new.items():
            if self.g.nodes[nid].value != val:
                self.g.nodes[nid].value = val; changed += 1
        return changed

    def run(self, active_anchor_ids, cfg: FixpointConfig) -> int:
        frames = self.anchors.active_frames(active_anchor_ids)
        weights = self.anchors.weights_for(active_anchor_ids)
        total = 0
        for i in range(cfg.max_iters):
            ch = self._step(frames, weights); total += ch
            if cfg.verbose: print(f"[Φ] iter {i+1} changed={ch}")
            if ch <= cfg.tol_changes: break
        return total
