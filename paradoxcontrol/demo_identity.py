from paradoxcontrol import load_anchors, select_and_stabilize, weave_anchor_block, quick_truth

if __name__ == "__main__":
    anchors = load_anchors()
    user_text = "This is about Zero-Day and legal artifacts."
    props = [
        ("P:RequiemIsMacie", "Requiem is Macie", [
            ("mythic", 0.8, +1),   # support
            ("legal",  0.7, -1),   # counter
        ])
    ]
    sel = select_and_stabilize(user_text, props, anchors, prefer_ids=["A04","A18"], k=5, verbose=True)
    print(weave_anchor_block(sel.anchors_used, anchors))
    for pid, tv in sel.values.items():
        print(pid, "=", quick_truth(tv))
