import json
import random
from pathlib import Path
from time import sleep, time

import cv2
import numpy as np
import pyautogui
from scipy.ndimage import center_of_mass, label

from runelite_library.rune_logger import log_event
from runelite_library.window_management import RuneLiteWindow
from too_many_items import PlayerObjects

CONFIG_FILE = Path("config.json")
with Path.open(CONFIG_FILE) as file:
    CONFIG = json.load(file)

REACTION_TIME_RANGES = {
    "fast": (0.05, 0.2),
    "medium": (0.1, 0.5),
    "slow": (0.5, 2),
}

INTERFACES = CONFIG["Interface_Shortcuts"]


class Interact:
    def __init__(
        self,
        rl: RuneLiteWindow,
        bounds: dict | None = None,
    ):
        self.rl = rl
        self.bounds = bounds or rl.whole_window

    @staticmethod
    def reaction_time():
        low, high = REACTION_TIME_RANGES[CONFIG["Reaction_Time"]]
        return random.uniform(low, high)

    @property
    def screenshot(self):
        return self.rl.capture(self.bounds)

    def find_by_color(self, rs_object: tuple, tolerance: int = 0):
        img = self.screenshot

        img_bgr = cv2.cvtColor(
            img[:, :, :3],
            cv2.COLOR_RGB2BGR,
        )

        lower = np.clip(
            np.array(rs_object) - tolerance,
            0,
            255,
        )

        upper = np.clip(
            np.array(rs_object) + tolerance,
            0,
            255,
        )

        mask = cv2.inRange(img_bgr, lower, upper)

        labeled_array, num_features = label(mask)

        if num_features == 0:
            return None

        centers = center_of_mass(
            mask,
            labeled_array,
            range(1, num_features + 1),
        )

        y_center, x_center = centers[0]

        return (
            int(x_center + self.bounds["left"]),
            int(y_center + self.bounds["top"]),
        )

    def find_by_image(
        self,
        rs_object: str,
        tolerance: int = 0.6,
    ):
        img = self.screenshot

        # Ensure screenshot is RGB and strip alpha if needed
        if img.shape[2] == 4:
            screenshot = img[:, :, :3]

        # Load the template and convert to RGB
        template = cv2.imread(rs_object, cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError

        th, tw = template.shape[:2]

        # Match in RGB space
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= tolerance:
            center_x = max_loc[0] + tw // 2 + self.bounds["left"]
            center_y = max_loc[1] + th // 2 + self.bounds["top"]
            return center_x, center_y

        return None

    def click(
        self,
        rs_object: tuple | str,
        click_type: str | None = None,
        mouse_tooltip: str | None = None,
        timeout: int = 10,
    ):
        """
        The bread and butter! Find object, move to, and click it!

        Args:
            rs_object: any object from `too_many_items`
            click_type: defaults to left click, but takes any of:
                - "right"
                - "double"
                - "middle"
            mouse_tooltip: any `ToolTip` object from `too_many_items`
            timeout: an integer in seconds

        """
        clicks_dict = {
            "default": pyautogui.click,
            "right": pyautogui.rightClick,
            "double": pyautogui.doubleClick,
            "middle": pyautogui.middleClick,
        }

        if click_type in clicks_dict:
            click = clicks_dict.get(click_type)
        else:
            click = clicks_dict.get("default")

        start_time = time()

        if isinstance(rs_object, tuple):
            func = self.find_by_color
        elif isinstance(rs_object, str):
            func = self.find_by_image

        while time() - start_time < timeout:
            try:
                x, y = func(rs_object)
            except TypeError:
                sleep(0.1)
                continue

            pyautogui.moveTo(
                x,
                y,
                duration=self.reaction_time(),
                tween=pyautogui.easeInOutQuad,
            )

            if mouse_tooltip:
                if self.find_by_image(mouse_tooltip):
                    log_event(
                        message=f"Found {mouse_tooltip}",
                        level="debug",
                    )
                else:
                    log_event(
                        message=f"Didn't find {mouse_tooltip} on screen.",
                        level="debug",
                    )
                    continue

            sleep(self.reaction_time())
            click()
            sleep(self.reaction_time())

            return True

        raise TimeoutError(f"Timed out waiting for {rs_object}")

    def find_all_by_color(
        self,
        rs_object: tuple,
        tolerance: int = 3,
        timeout: int = 15,
    ) -> list[tuple]:
        img = self.screenshot
        start_time = time()

        while time() - start_time < timeout:
            img_bgr = cv2.cvtColor(img[:, :, :3], cv2.COLOR_RGB2BGR)

            # Generate mask
            lower = np.clip(np.array(rs_object) - tolerance, 0, 255)
            upper = np.clip(np.array(rs_object) + tolerance, 0, 255)
            mask = np.all(
                (img_bgr[:, :, :3] >= lower) & (img_bgr[:, :, :3] <= upper),
                axis=-1,
            )
            if not np.any(mask):
                continue

            labeled_array, num_features = label(mask.astype(np.uint8))
            if num_features == 0:
                continue

            centers = center_of_mass(mask, labeled_array, range(1, num_features + 1))
            return [
                (int(xc + self.bounds["left"]), int(yc + self.bounds["top"]))
                for yc, xc in centers
            ]

        return []

    def find_all_by_image(
        self,
        rs_object: str,
        tolerance: int = 0.8,
    ) -> list[tuple]:
        img = self.screenshot
        if img.shape[2] == 4:
            img = img[:, :, :3]

        template = cv2.imread(rs_object, cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError

        th, tw = template.shape[:2]

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Get all locations above the threshold
        ys, xs = np.where(result >= tolerance)

        matches = []
        for x, y in zip(xs, ys, strict=True):
            center_x = x + tw // 2 + self.bounds["left"]
            center_y = y + th // 2 + self.bounds["top"]
            matches.append((int(center_x), int(center_y)))

        return matches

    def count_object(self, rs_object: str | tuple) -> int:
        if isinstance(rs_object, str):
            func = self.find_all_by_image
        elif isinstance(rs_object, tuple):
            func = self.find_all_by_color
        return len(func(rs_object))

    def click_all_object(self, rs_object: str | tuple) -> bool:
        if isinstance(rs_object, str):
            func = self.find_all_by_image
        if isinstance(rs_object, tuple):
            func = self.find_all_by_color

        for match in func(rs_object):
            x, y = match
            pyautogui.moveTo(
                x,
                y,
                duration=self.reaction_time(),
                tween=pyautogui.easeInOutQuad,
            )
            sleep(0.03)
            pyautogui.click()

    def random_coordinate_in_area(self) -> tuple:
        rand_x = random.randint(0, self.bounds["width"] - 1)
        rand_y = random.randint(0, self.bounds["height"] - 1)

        absolute_x = self.bounds["left"] + rand_x
        absolute_y = self.bounds["top"] + rand_y

        return (absolute_x, absolute_y)

    def find_player(self) -> tuple:
        return self.find_by_color(PlayerObjects.player_tile)

    def wait_for_element(self, rs_object: tuple | str, timeout: int = 15) -> bool:
        start_time = time()

        if isinstance(rs_object, tuple):
            func = self.find_by_color
        elif isinstance(rs_object, str):
            func = self.find_by_image

        while time() - start_time < timeout:
            if func(rs_object):
                return True

        return False


class RuneliteComponent:
    def __init__(self, rl: RuneLiteWindow):
        self.rl = rl
        self.logout = Interact(self.rl, self.rl.logout)
        self.client = Interact(self.rl)
        self.play_window = Interact(self.rl, self.rl.play_area)
        self.inventory = Interact(self.rl, self.rl.inventory)
        self.minimap = Interact(self.rl, self.rl.minimap)
        self.compass = Interact(self.rl, self.rl.compass)


# - - - - - - - #
#  Standalone   #
# - - - - - - - #


def move_to_and_click(coordinates: tuple):
    x, y = coordinates
    pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    sleep(0.03)
    pyautogui.click()


def click_compass(rl: RuneLiteWindow):
    bounds = rl.compass

    x1 = bounds["left"]
    y1 = bounds["top"]
    width = bounds["width"]
    height = bounds["height"]

    center_x = x1 + width // 2
    center_y = y1 + height // 2
    move_to_and_click((center_x, center_y))


def pan_up():
    pyautogui.keyDown("up")
    sleep(4)
    pyautogui.keyUp("up")


def scroll_out(rl: RuneLiteWindow):
    bounds = rl.play_area

    x1 = bounds["left"]
    y1 = bounds["top"]
    width = bounds["width"]
    height = bounds["height"]

    x = int(random.uniform(x1, x1 + width))
    y = int(random.uniform(y1, y1 + height))

    pyautogui.moveTo(
        x,
        y,
        duration=0.2,
        tween=pyautogui.easeInOutQuad,
    )
    pyautogui.scroll(clicks=-4500)


def set_screen(rl):
    click_compass(rl)
    pan_up()
    scroll_out(rl)


def open_interface(interface: str):
    """
    Uses F-Key shortcuts to open menus. Configured in config.json.

    Args:
        interface (str): The interface to open. Must be one of:
            - "inventory"
            - "stats"
            - "spells"
            - "equipment"
            - "quests"
            - "logout"
            - "emotes"
            - "prayer"
            - "combat"
            - "grouping"

    Raises:
        KeyError: If the interface is not valid

    """
    if interface not in INTERFACES:
        raise KeyError
    pyautogui.press(INTERFACES[interface])


def close_interface():
    pyautogui.press("esc")
