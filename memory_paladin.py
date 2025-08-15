"""Memory guardian that checksums important files."""
from __future__ import annotations

import hashlib
import json
import os
from typing import Dict, List


class MemoryPaladin:
    def __init__(self, files: List[str], record_file: str = "paladin.json") -> None:
        self.files = files
        self.record_file = record_file
        self.records: Dict[str, str] = self._load()
        self.update_records()

    def _load(self) -> Dict[str, str]:
        try:
            with open(self.record_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _checksum(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def update_records(self) -> None:
        for f in self.files:
            if os.path.exists(f):
                self.records[f] = self._checksum(f)
        with open(self.record_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

    def verify(self) -> bool:
        for f, sig in self.records.items():
            if os.path.exists(f) and self._checksum(f) != sig:
                return False
        return True
