import json
from memory_paladin import MemoryPaladin


def test_memory_paladin_detects_change(tmp_path):
    f = tmp_path / "data.json"
    f.write_text("a")
    pal = MemoryPaladin([str(f)], record_file=str(tmp_path / "rec.json"))
    assert pal.verify()
    f.write_text("b")
    assert not pal.verify()
