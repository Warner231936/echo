from resource_manager import ResourceManager


def test_resource_manager_sample():
    rm = ResourceManager()
    data = rm.sample()
    assert {
        "cpu",
        "memory",
        "net_in",
        "net_out",
        "load",
    } <= data.keys()
