import subprocess

import mss
import numpy as np


class RuneLiteWindow:
    def __init__(self) -> None:
        self.window_id = None
        self.player_name = None

    def _find_window(self) -> None:
        result = subprocess.check_output(["/usr/bin/wmctrl", "-l"]).decode()

        for line in result.splitlines():
            if "runelite" in line.lower():
                self.player_name = line.split("-")[1].lstrip()
                return line.split()[0]

        return None

    def activate(self) -> None:
        """Finds and activates the RuneLite window."""
        self.window_id = self._find_window()
        if not self.window_id:
            raise RuntimeError("RuneLite window not found")

        subprocess.run(["/usr/bin/wmctrl", "-i", "-a", self.window_id], check=True)  # noqa: S603

    def _get_bounds(self) -> tuple:
        if not self.window_id:
            self.activate()

        bounds = subprocess.check_output(  # noqa: S603
            ["/usr/bin/xdotool", "getwindowgeometry", "--shell", self.window_id],
        ).decode()

        values = {}
        for line in bounds.splitlines():
            key, val = line.split("=")
            values[key] = int(val)

        x1 = values["X"]
        y1 = values["Y"]
        x2 = x1 + values["WIDTH"]
        y2 = y1 + values["HEIGHT"]

        return x1, y1, x2, y2

    def capture(self, area=None, file_name=None):
        self._ensure_window()

        if area is None:
            x1, y1, x2, y2 = self.bounds

            area = {
                "top": y1,
                "left": x1,
                "width": x2 - x1,
                "height": y2 - y1,
            }

        with mss.mss() as sct:
            screenshot = sct.grab(area)
            img_np = np.array(screenshot)

            if file_name:
                mss.tools.to_png(
                    screenshot.rgb,
                    screenshot.size,
                    output=file_name,
                )

            return img_np

    def _ensure_window(self):
        if not self.window_id:
            self.activate()

    @property
    def bounds(self):
        self._ensure_window()

        bounds = subprocess.check_output(  # noqa: S603
            [
                "/usr/bin/xdotool",
                "getwindowgeometry",
                "--shell",
                self.window_id,
            ],
        ).decode()

        values = {}
        for line in bounds.splitlines():
            key, val = line.split("=")
            values[key] = int(val)

        x1 = values["X"]
        y1 = values["Y"]
        x2 = x1 + values["WIDTH"]
        y2 = y1 + values["HEIGHT"]

        return x1, y1, x2, y2

    # ----------------------------
    # Areas
    # ----------------------------

    @property
    def inventory(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 300,
            "left": x2 - 260,
            "width": 220,
            "height": 265,
        }

    @property
    def play_area(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1,
            "left": x1,
            "width": (x2 - x1) - 265,
            "height": (y2 - y1) - 25,
        }

    @property
    def minimap(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1 + 25,
            "left": x2 - 165,
            "width": 100,
            "height": 115,
        }

    @property
    def compass(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1 + 15,
            "left": x2 - 200,
            "width": 20,
            "height": 20,
        }

    @property
    def inv_slot_28(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 77,
            "left": x2 - 107,
            "width": 40,
            "height": 40,
        }

    @property
    def health(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1 + 56,
            "left": x2 - 210,
            "width": 17,
            "height": 16,
        }

    @property
    def whole_window(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1,
            "left": x1,
            "width": x2 - x1,
            "height": y2 - y1,
        }

    @property
    def fishing_trawler(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 126,
            "left": x2 - 233,
            "width": 80,
            "height": 12,
        }

    @property
    def minigame_teleport(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 52,
            "left": x2 - 120,
            "width": 50,
            "height": 12,
        }

    @property
    def logout(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 80,
            "left": x2 - 200,
            "width": 100,
            "height": 20,
        }

    @property
    def home_teleport(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y2 - 280,
            "left": x2 - 230,
            "width": 15,
            "height": 15,
        }

    @property
    def prayer(self):
        x1, y1, x2, y2 = self.bounds

        return {
            "top": y1 + 86,
            "left": x2 - 212,
            "width": 20,
            "height": 24,
        }
