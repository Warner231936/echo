from paradoxcontrol import load_anchors, select_and_stabilize, weave_anchor_block, TV

def test_paradox_control_demo():
    anchors = load_anchors()
    user_text = "This is about Zero-Day and legal artifacts."
    props = [
        ("P:RequiemIsMacie", "Requiem is Macie", [
            ("mythic", 0.8, +1),   # support
            ("legal", 0.7, -1),    # counter
        ])
    ]
    sel = select_and_stabilize(user_text, props, anchors, prefer_ids=["A04","A18"], k=5)
    assert "P:RequiemIsMacie" in sel.values
    assert sel.values["P:RequiemIsMacie"] == TV.B
    block = weave_anchor_block(sel.anchors_used, anchors)
    assert "### ACTIVE ANCHORS" in block
    assert "Reflection of the Forgotten Self" in block
