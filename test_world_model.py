from world_model import WorldModel

def test_sensor_polling():
    wm = WorldModel()
    wm.register_sensor("test", lambda: 42)
    wm.poll_senses()
    assert wm.senses["test"] == 42
