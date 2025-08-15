from self_tuner import ReflectionTrainer

def test_record(tmp_path):
    path = tmp_path / "train.txt"
    rt = ReflectionTrainer(str(path))
    rt.record("hello world")
    assert path.read_text().strip() == "hello world"
