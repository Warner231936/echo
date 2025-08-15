from theory_of_mind import TheoryOfMind

def test_infer_emotion():
    tom = TheoryOfMind()
    assert tom.infer("I am very happy today") == "happy"
    assert tom.infer("I feel sad") == "sad"
