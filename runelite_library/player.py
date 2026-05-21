from time import sleep

import requests

from runelite_library.interact import RuneliteComponent
from too_many_items import PathingObjects

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
    def get_player_stats(self) -> dict:
        stats_request = requests.get(url="http://127.0.0.1:8080/stats", timeout=5)
        stats = {}
        for query in stats_request.json():
            stat_name = query["stat"]
            stat_level = query["level"]
            stats[stat_name.lower()] = stat_level

        return stats

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
