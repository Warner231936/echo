import os
from pathlib import Path
from self_preservation import SelfPreservation


def test_backup_and_detect(tmp_path):
    state = tmp_path / "state.json"
    state.write_text("{}", encoding="utf-8")
    sp = SelfPreservation([str(state)], backup_dir=str(tmp_path / "bk"))
    sp.backup()
    backups = list((tmp_path / "bk").glob("*") )
    assert backups, "backup file missing"
    state.write_text('{"a":1}', encoding="utf-8")
    threats = sp.detect_threats()
    assert any("modified" in t for t in threats)
