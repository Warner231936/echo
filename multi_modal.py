"""Basic multimodal helpers."""

from typing import Dict, Any

try:  # optional dependency
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

class MultiModal:
    """Provide lightweight multimodal processing."""

    def process_image(self, path: str) -> Dict[str, Any]:
        if not Image:
            raise RuntimeError("Pillow not installed")
        with Image.open(path) as img:
            return {"size": img.size, "mode": img.mode}

    # Stub helpers for audio and video so the world model can sense them
    def process_audio(self, path: str) -> Dict[str, Any]:
        return {"audio": path}

    def process_video(self, path: str) -> Dict[str, Any]:
        return {"video": path}
