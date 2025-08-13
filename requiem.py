import time
import json
import threading
import subprocess
from dataclasses import dataclass, field
from typing import List, Dict, Any

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


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

    def __init__(self, ltm_file: str = "ltm.json", heartbeat: int = 5):
        self.stm: List[MemoryItem] = []
        self.ltm_file = ltm_file
        self.ltm: List[MemoryItem] = self._load_ltm()
        self.policy = PolicyEngine()
        self.heartbeat_interval = heartbeat
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

    def _heartbeat(self) -> None:
        thought = {
            "thought": f"tick at {time.ctime()}"
        }
        self._store(MemoryItem(time.time(), thought))
        self._start_heartbeat()

    # --------------- public API ----------------
    def receive_input(self, text: str) -> str:
        self._store(MemoryItem(time.time(), {"user": text}))
        if not self.policy.allowed(text):
            reply = "This request conflicts with my policies."
        else:
            reply = f"Echo: {text}"
        self._store(MemoryItem(time.time(), {"assistant": reply}))
        return reply

    def run_command(self, cmd: str) -> str:
        """Execute a shell command and return its output."""
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self._store(MemoryItem(time.time(), {"cmd": cmd}))
        return proc.stdout + proc.stderr

    def http_get(self, url: str) -> str:
        if requests is None:
            raise RuntimeError("requests library not available")
        resp = requests.get(url, timeout=5)
        self._store(MemoryItem(time.time(), {"http": url}))
        return resp.text[:200]


if __name__ == "__main__":
    rq = Requiem()
    print("Requiem ready. Type 'exit' to quit.")
    while True:
        try:
            text = input("you> ")
        except (EOFError, KeyboardInterrupt):
            break
        if text.strip().lower() == "exit":
            break
        print("rq>", rq.receive_input(text))
