from world_model import WorldModel


def test_audio_video_senses():
    wm = WorldModel()
    wm.hear_audio('a.wav')
    wm.watch_video('v.mp4')
    assert 'audio' in wm.senses and 'video' in wm.senses
