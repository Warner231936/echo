from social_context import SocialContext


def test_style_changes():
    ctx = SocialContext()
    for _ in range(6):
        ctx.record("bob", "hi")
    assert ctx.style_for("bob") == "friendly"
    ctx.record("Macie", "command")
    assert ctx.style_for("Macie") == "formal"
