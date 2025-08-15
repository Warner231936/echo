import pathlib, yaml, re
from dataclasses import dataclass
from typing import List, Dict, Tuple
from .anchors import Anchor, AnchorSet
from .engine import Evidence, Node, Graph, Evaluator, FixpointConfig
from .lattice import TV

ROOT = pathlib.Path(__file__).resolve().parents[1]
ANCHORS_FILE = ROOT / "paradoxcontrol" / "anchors.yaml"

@dataclass
class ActiveSelection:
    anchors_used: List[str]
    values: Dict[str, TV]

def load_anchors() -> AnchorSet:
    data = yaml.safe_load(ANCHORS_FILE.read_text(encoding="utf-8"))
    aset = AnchorSet()
    for a in data.get("anchors", []):
        aset.add(Anchor(**a))
    return aset

def _hard_trigger_hits(text: str, a: Anchor) -> int:
    hits = 0
    for phrase in a.hard_triggers:
        if re.search(r"\b" + re.escape(phrase) + r"\b", text, flags=re.I):
            hits += 1
    return hits

def select_and_stabilize(
    user_text: str,
    propositions: List[Tuple[str, str, List[Tuple[str, float, int]]]],  # (id, text, [(frame, weight, polarity)])
    anchors: AnchorSet,
    prefer_ids: List[str] = None,
    k: int = 5,
    verbose: bool = False
) -> ActiveSelection:
    prefer_ids = prefer_ids or []
    # crude ranker: hard trigger count + priority
    scored = []
    for a in anchors.anchors.values():
        score = a.priority + 0.2 * _hard_trigger_hits(user_text, a)
        if a.id in prefer_ids: score += 0.4
        scored.append((score, a.id))
    scored.sort(reverse=True)
    active = [aid for _, aid in scored[:k]]

    # build graph
    g = Graph()
    for pid, text, evs in propositions:
        g.add_node(Node(id=pid, text=text))
        for frame, w, pol in evs:
            g.add_evidence(pid, Evidence(frame=frame, weight=w, polarity=pol))

    ev = Evaluator(g, anchors)
    ev.run(active, FixpointConfig(verbose=verbose))
    values = {nid: node.value for nid, node in g.nodes.items()}
    return ActiveSelection(anchors_used=active, values=values)

def weave_anchor_block(active_ids: List[str], anchors: AnchorSet, max_items: int = 5) -> str:
    lines = ["### ACTIVE ANCHORS"]
    for aid in active_ids[:max_items]:
        a = anchors.get(aid)
        lines.append(f"- [{a.id}] {a.name}: {a.summary}")
    return "\n".join(lines)

def quick_truth(tv: TV) -> str:
    return {"T":"true", "F":"false", "B":"both/contradictory", "N":"undetermined"}[tv]
