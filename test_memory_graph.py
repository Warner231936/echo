from memory_graph import MemoryGraph

def test_graph_links(tmp_path):
    path = tmp_path / "graph.json"
    mg = MemoryGraph(path=str(path))
    mg.add_statement("sky is blue")
    mg.add_statement("blue is calming")
    assert "blue" in mg.related("sky")
    assert "sky" in mg.related("calming")
