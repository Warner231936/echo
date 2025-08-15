from social_env import SocialEnvironment

def test_social_message():
    env = SocialEnvironment(["A", "B"])
    env.send("A", "B", "hi")
    assert env.agents["B"].inbox == [("A", "hi")]
    assert env.history[-1] == ("A", "B", "hi")
