from time import sleep

import numpy as np
import requests

from config import settings
from custom_dataclasses import Account
from runelite_library.database import NullDatabase, RuneDashboard
from runelite_library.interact import RuneliteComponent
from too_many_items import PathingObjects, PlayerObjects

DATABASE = RuneDashboard if settings.use_database else NullDatabase


PATH_OBJECTS = {
    1: PathingObjects.step_1,
    2: PathingObjects.step_2,
    3: PathingObjects.step_3,
    4: PathingObjects.step_4,
    5: PathingObjects.step_5,
    6: PathingObjects.step_6,
    7: PathingObjects.step_7,
    8: PathingObjects.step_8,
    9: PathingObjects.step_9,
    10: PathingObjects.step_10,
}


class Player(RuneliteComponent):
    def __init__(self, rl):
        super().__init__(rl)
        self.d = DATABASE()

    def get_player_stats(self) -> dict:
        stats_request = requests.get(url="http://127.0.0.1:8080/stats", timeout=5)
        stats = {}
        for query in stats_request.json():
            stat_name = query["stat"]
            stat_level = query["level"]
            stats[stat_name.lower()] = stat_level

        return stats

    def update_player_stats(self, account_name, account_id: int) -> int:
        stats = self.get_player_stats()
        new_account = Account(account_name)

        setattr(new_account, "attack_level", stats["attack"])
        setattr(new_account, "defence_level", stats["defence"])
        setattr(new_account, "strength_level", stats["strength"])
        setattr(new_account, "hitpoints_level", stats["hitpoints"])
        setattr(new_account, "ranged_level", stats["ranged"])
        setattr(new_account, "prayer_level", stats["prayer"])
        setattr(new_account, "magic_level", stats["magic"])
        setattr(new_account, "cooking_level", stats["cooking"])
        setattr(new_account, "woodcutting_level", stats["woodcutting"])
        setattr(new_account, "fletching_level", stats["fletching"])
        setattr(new_account, "fishing_level", stats["fishing"])
        setattr(new_account, "firemaking_level", stats["firemaking"])
        setattr(new_account, "crafting_level", stats["crafting"])
        setattr(new_account, "smithing_level", stats["smithing"])
        setattr(new_account, "mining_level", stats["mining"])
        setattr(new_account, "herblore_level", stats["herblore"])
        setattr(new_account, "agility_level", stats["agility"])
        setattr(new_account, "thieving_level", stats["thieving"])
        setattr(new_account, "slayer_level", stats["slayer"])
        setattr(new_account, "farming_level", stats["farming"])
        setattr(new_account, "runecraft_level", stats["runecraft"])
        setattr(new_account, "hunter_level", stats["hunter"])
        setattr(new_account, "construction_level", stats["construction"])
        setattr(new_account, "sailing_level", stats["sailing"])

        return self.d.patch_player_stats(new_account, account_id)

    def stat_level(self, stat: str):
        stat = stat.lower()
        player_stats = self.get_player_stats()
        return player_stats[stat]

    def get_player_inv(self) -> dict:
        inv_request = requests.get(url="http://127.0.0.1:8080/inv", timeout=5)
        # inv = {}
        print(inv_request.json())

    def path_to(self, path: int, rest: int = 0):
        """
        From step_1, paths up to inputted path number using minimap.

        Args:
            path (int): The path number to step up to. Max value of 10!
            rest (int): The amount of time in seconds to wait between checks. Defaults to 0.

        Raises:
            ValueError: if path is out of bounds.

        """
        if path < 1 or path > 10:
            raise ValueError("The value of path should be between 1 and 10 inclusive.")

        step = 1

        while step <= path:
            if not self.minimap.click(PATH_OBJECTS.get(step)):
                return False
            step += 1
            sleep(rest)

        return True

    def step_to(self, step):
        if step < 1 or step > 10:
            raise ValueError("The value of step should be between 1 and 10 inclusive.")
        return self.minimap.click(PATH_OBJECTS.get(step))

    def get_player_id(self) -> int | None:
        response = self.d.get_player_by_name(self.rl.player_name)

        if response.status_code == 404:
            player = self.d.create_player(self.rl.player_name)
            return player.json()["id"]

        if response.status_code == 200:
            return response.json()["id"]

        return None

    @property
    def prayer(self) -> tuple[int, int, int]:
        current_rgb = self.player_prayer.average_color_of_area()

        full_prayer = np.array([91, 75, 78])
        empty_prayer = np.array([61, 63, 60])

        current = np.array(current_rgb)

        direction = full_prayer - empty_prayer

        progress = np.dot(
            current - empty_prayer,
            direction,
        ) / np.dot(direction, direction)

        return int(max(0.0, min(100.0, progress * 100)))

    @property
    def health(self) -> tuple[int, int, int]:
        """Less than 30% is low health"""
        current_rgb = self.player_health.average_color_of_area()

        most_health = np.array([7, 24, 131])
        low_health = np.array([12, 28, 85])

        current = np.array(current_rgb)

        direction = most_health - low_health

        progress = np.dot(
            current - low_health,
            direction,
        ) / np.dot(direction, direction)

        return int(max(0.0, min(100.0, progress * 100)))

    @property
    def inventory_full(self) -> bool:
        current_rgb = self.last_inventory_slot.average_color_of_area()
        return current_rgb != PlayerObjects.last_inv
