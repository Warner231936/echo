import time
import json
import threading
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from llm import load_llm


@dataclass
class MemoryItem:
    timestamp: float
    data: Dict[str, Any]


class PolicyEngine:
    """Very small placeholder for a moral/ethical policy."""

    banned_words = {"harm", "attack"}

    def allowed(self, text: str) -> bool:
        return not any(word in text.lower() for word in self.banned_words)


class Requiem:
    """Prototype core system for an AI assistant with memory and a heartbeat."""

    def __init__(
        self,
        ltm_file: str = "ltm.json",
        heartbeat: int = 5,
        llm: Optional[object] = None,
        model: str = "mistral-tiny",
    ) -> None:
        self.stm: List[MemoryItem] = []
        self.ltm_file = ltm_file
        self.ltm: List[MemoryItem] = self._load_ltm()
        self.policy = PolicyEngine()
        self.heartbeat_interval = heartbeat
        self.model = model
        self.llm = llm or load_llm(model)
        self._start_heartbeat()

    # ------------------ memory ------------------
    def _load_ltm(self) -> List[MemoryItem]:
        try:
            with open(self.ltm_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [MemoryItem(**item) for item in data]
        except FileNotFoundError:
            return []

    def _save_ltm(self) -> None:
        with open(self.ltm_file, "w", encoding="utf-8") as f:
            json.dump([item.__dict__ for item in self.ltm], f, indent=2)

    def _store(self, item: MemoryItem) -> None:
        self.stm.append(item)
        if len(self.stm) > 50:
            # summarize oldest item into long-term memory
            self.ltm.append(self.stm.pop(0))
            self._save_ltm()

    # ---------------- heartbeat -----------------
    def _start_heartbeat(self) -> None:
        self._hb = threading.Timer(self.heartbeat_interval, self._heartbeat)
        self._hb.daemon = True
        self._hb.start()
@@ -100,82 +85,55 @@ class Requiem:
        """Process user input and generate a simple response."""
        self._store(MemoryItem(time.time(), {"user": text}))

        if not self.policy.allowed(text):
            reply = "This request conflicts with my policies."

        elif text.lower().startswith("remember "):
            # allow the user to explicitly store memories
            memory = text[len("remember ") :].strip()
            self._store(MemoryItem(time.time(), {"note": memory}))
            reply = "I'll remember that."

        elif "what do you remember" in text.lower():
            notes = [item.data["note"] for item in self.ltm + self.stm if "note" in item.data]
            reply = "I recall: " + "; ".join(notes[-3:]) if notes else "I don't have any memories yet."

        elif "time" in text.lower():
            reply = f"It's {time.ctime()}"

        else:
            # reference the previous user message if available
            last_user = next(
                (item.data["user"] for item in reversed(self.stm[:-1]) if "user" in item.data),
                None,
            )
            reply = self.llm.reply(text, last_user)

        self._store(MemoryItem(time.time(), {"assistant": reply}))
        return reply
