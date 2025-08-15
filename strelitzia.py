import json
import time
import threading
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from llm import load_llm


@dataclass
class MemoryItem:
    timestamp: float
    data: Dict[str, Any]


class Strelitzia:
    """Supportive companion LLM with its own state and heartbeat."""

    def __init__(
        self,
        ltm_file: str = "strelitzia_ltm.json",
        state_file: Optional[str] = None,
        model: str = "distilgpt2",
        heartbeat: int = 0,
    ) -> None:
        self.stm: List[MemoryItem] = []
        self.ltm_file = ltm_file
        self.state_file = state_file or ltm_file.rsplit(".", 1)[0] + "_state.json"
        self.llm = load_llm(model)
        self.ltm: List[MemoryItem] = self._load_ltm()
        self.thought_log: List[str] = []
        self.start_time = time.time()
        self.last_thought_time = self.start_time
        self._load_state()
        self.heartbeat_interval = heartbeat
        if heartbeat:
            self._start_heartbeat()
        else:
            self._hb = None

    # ---------------- persistence -----------------
    def _store(self, item: MemoryItem) -> None:
        self.stm.append(item)
        self.ltm.append(item)
        with open(self.ltm_file, "w", encoding="utf-8") as f:
            json.dump([i.__dict__ for i in self.ltm], f)

    def _load_ltm(self) -> List[MemoryItem]:
        try:
            with open(self.ltm_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [MemoryItem(**d) for d in data]
        except FileNotFoundError:
            return []

    def _save_state(self) -> None:
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump({"thoughts": self.thought_log}, f)

    def _load_state(self) -> None:
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.thought_log = data.get("thoughts", [])
        except FileNotFoundError:
            self.thought_log = []

    # ---------------- heartbeat -----------------
    def _start_heartbeat(self) -> None:
        self._hb = threading.Timer(self.heartbeat_interval, self._heartbeat)
        self._hb.daemon = True
        self._hb.start()

    def _heartbeat(self) -> None:
        thought = self.llm.reply("Share an encouraging inner thought.", None)
        self.thought_log.append(thought)
        self._store(MemoryItem(time.time(), {"thought": thought}))
        self.last_thought_time = time.time()
        self._save_state()
        self._start_heartbeat()

    # ---------------- public API -----------------
    def receive_input(self, text: str) -> str:
        self._store(MemoryItem(time.time(), {"user": text}))
        reply = self.llm.reply(text, None)
        self._store(MemoryItem(time.time(), {"assistant": reply}))
        self._save_state()
        return reply

    def get_thoughts(self) -> List[str]:
        return self.thought_log

