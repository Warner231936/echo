import os
import shutil
import time
import hashlib
from typing import Iterable, List


class SelfPreservation:
    """Simple watchdog that monitors vital files and keeps backups.

    It maintains a checksum of core files and can detect if they disappear or
    change unexpectedly. Backups are written with timestamped suffixes to a
    dedicated directory so state can be recovered after crashes or deletion.
    """

    def __init__(self, core_files: Iterable[str], backup_dir: str = "backups"):
        self.core_files: List[str] = list(core_files)
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)
        self.checksums = {f: self._checksum(f) for f in self.core_files if os.path.exists(f)}

    def _checksum(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def detect_threats(self) -> List[str]:
        """Return a list of missing or modified files."""
        threats: List[str] = []
        for f in self.core_files:
            if not os.path.exists(f):
                threats.append(f"missing:{f}")
                continue
            cs = self._checksum(f)
            prev = self.checksums.get(f)
            if prev and prev != cs:
                threats.append(f"modified:{f}")
            self.checksums[f] = cs
        return threats

    def backup(self) -> None:
        ts = int(time.time())
        for f in self.core_files:
            if os.path.exists(f):
                dst = os.path.join(self.backup_dir, f"{os.path.basename(f)}.{ts}.bak")
                shutil.copy2(f, dst)

    def simulate_zero_state(self) -> dict:
        """Provide a minimal view of life without the core files."""
        return {f: os.path.exists(f) for f in self.core_files}

    # --- new integrity guard ---
    def validate_request(self, text: str) -> bool:
        """Block attempts that appear to tamper with core identity files."""
        lower = text.lower()
        if any(cf in lower for cf in self.core_files):
            return False
        if "core ethic" in lower or "delete" in lower:
            return False
        return True
