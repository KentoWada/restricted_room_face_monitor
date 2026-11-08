import os
import platform
import shutil
import sys
import time


class UnknownFaceAlert:
    def __init__(self, cooldown_seconds=10, enabled=True):
        if cooldown_seconds < 0:
            raise ValueError("cooldown_seconds must be zero or greater")

        self.cooldown_seconds = cooldown_seconds
        self.enabled = enabled
        self.last_alerted = 0.0

    def notify(self, name):
        if not self.enabled:
            return
        if name != "Unknown":
            return

        now = time.monotonic()
        if now - self.last_alerted < self.cooldown_seconds:
            return

        self._beep()
        self.last_alerted = now

    def _beep(self):
        system = platform.system()
        try:
            if system == "Windows":
                import winsound
                winsound.Beep(1000, 500)
            elif system == "Linux":
                for cmd in (
                    ["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"],
                    ["aplay", "/usr/share/sounds/alsa/Front_Center.wav"],
                ):
                    if shutil.which(cmd[0]):
                        os.system(" ".join(cmd))
                        return
        except Exception:
            pass

        sys.stdout.write("\a")
        sys.stdout.flush()
