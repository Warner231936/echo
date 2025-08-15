"""Dynamic registry for external helper agents.

Extended to support remote agents declared by URL. If an agent target in the
configuration begins with ``http://`` or ``https://`` the registry will create a
callable that POSTs the task to the remote endpoint and returns the ``result``
field from the JSON response. This provides a simple building block for a
distributed or swarm‑style architecture where helper agents can live on other
machines.
"""
from __future__ import annotations
import importlib
import json
from pathlib import Path
from typing import Callable, Dict

import requests

class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, Callable[[str], str]] = {}

    def register(self, name: str, handler: Callable[[str], str]) -> None:
        self._agents[name] = handler

    def unregister(self, name: str) -> None:
        self._agents.pop(name, None)

    def get(self, name: str) -> Callable[[str], str] | None:
        return self._agents.get(name)

    def names(self) -> Dict[str, Callable[[str], str]]:
        return dict(self._agents)

    def load_config(self, path: str) -> None:
        cfg = Path(path)
        if not cfg.exists():
            return
        data = json.loads(cfg.read_text())
        for name, target in data.items():
            if target.startswith("http://") or target.startswith("https://"):
                def handler(task: str, url=target) -> str:
                    response = requests.post(url, json={"task": task}, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    return data.get("result", "")
                self.register(name, handler)
            else:
                module_name, func_name = target.rsplit(":", 1)
                mod = importlib.import_module(module_name)
                handler = getattr(mod, func_name)
                self.register(name, handler)
