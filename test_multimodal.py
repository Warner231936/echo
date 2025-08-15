from world_model import WorldModel
from PIL import Image

def test_see_image(tmp_path):
    img_path = tmp_path / "img.png"
    Image.new("RGB", (1, 1), color="white").save(img_path)
    wm = WorldModel()
    data = wm.see_image(str(img_path))
    assert data["size"] == (1, 1)
