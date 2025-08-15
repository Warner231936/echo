from self_preservation import SelfPreservation

def test_validate_request_blocks_core(tmp_path):
    sp = SelfPreservation(["core.txt"], backup_dir=str(tmp_path))
    assert not sp.validate_request("delete core.txt")
    assert sp.validate_request("say hello")
