"""World model with pluggable sensors and proprioception."""

from typing import Dict, Any, Callable

from multi_modal import MultiModal


class WorldModel:
    """Continuously updated representation of Requiem's environment."""

    def __init__(self) -> None:
        self.senses: Dict[str, Any] = {}
        self.internal_state: Dict[str, Any] = {"status": "idle", "last_action": "none"}
        self._sensors: Dict[str, Callable[[], Any]] = {}
        self._multi = MultiModal()

    def register_sensor(self, name: str, func: Callable[[], Any]) -> None:
        """Register a callable that returns sensor data when polled."""
        self._sensors[name] = func

    def poll_senses(self) -> None:
        for name, func in list(self._sensors.items()):
            try:
                self.senses[name] = func()
            except Exception:
                # sensor failure shouldn't break heartbeat
                self.senses[name] = "error"

    def update_sense(self, name: str, data: Any) -> None:
        self.senses[name] = data

    def report(self) -> Dict[str, Any]:
        return {**self.senses, **self.internal_state}

    def set_action(self, action: str) -> None:
        self.internal_state["status"] = action
        self.internal_state["last_action"] = action

    # multimodal helpers

    def see_image(self, path: str) -> Dict[str, Any]:
        """Process an image file and record a vision sense."""
        data = self._multi.process_image(path)
        self.update_sense("vision", data)
        return data

    def hear_audio(self, path: str) -> Dict[str, Any]:
        """Process an audio file and record an audio sense."""
        data = self._multi.process_audio(path)
        self.update_sense("audio", data)
        return data

    def watch_video(self, path: str) -> Dict[str, Any]:
        """Process a video file and record a video sense."""
        data = self._multi.process_video(path)
        self.update_sense("video", data)
        return data
