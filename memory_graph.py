"""Simple relational memory graph for Requiem."""
from __future__ import annotations
import json
from typing import Dict, Set, List

class MemoryGraph:
    """Store facts as subject-relation-object triples and link related concepts."""

    def __init__(self, path: str = "ltm_graph.json") -> None:
        self.path = path
        self.graph: Dict[str, Dict[str, Set[str]]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Set[str]]]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {s: {r: set(objs) for r, objs in rels.items()} for s, rels in data.items()}
        except Exception:
            return {}

    def _save(self) -> None:
        data = {s: {r: list(objs) for r, objs in rels.items()} for s, rels in self.graph.items()}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_statement(self, text: str) -> None:
        """Very naive parser linking 'X is Y' style statements."""
        parts = text.lower().split(" is ")
        if len(parts) == 2:
            subj, obj = parts[0].strip(), parts[1].strip().strip('.')
            self.graph.setdefault(subj, {}).setdefault("is", set()).add(obj)
            # link back
            self.graph.setdefault(obj, {}).setdefault("related_to", set()).add(subj)
            # propagate indirect links: anyone that is subj becomes related to obj
            for other, rels in self.graph.items():
                if obj in rels.get("is", set()):
                    self.graph.setdefault(other, {}).setdefault("related_to", set()).add(subj)
            for other, rels in self.graph.items():
                if subj in rels.get("is", set()):
                    self.graph.setdefault(obj, {}).setdefault("related_to", set()).add(other)
            self._save()

    def related(self, concept: str) -> List[str]:
        rels = self.graph.get(concept.lower(), {})
        out: List[str] = []
        for objs in rels.values():
            out.extend(sorted(objs))
        return out
