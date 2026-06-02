import random
from datetime import datetime, time
from time import sleep

from custom_dataclasses import BirdhouseRun as Run
from runelite_library.database import create_player, get_player_by_name, submit_bird_run
from runelite_library.login import LoginLogout
from runelite_library.tracker import TrackTask
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun
from tasks.crafting import MoltenGlass


def random_interval():
    return int(random.uniform(50, 60))


def bedtime():
    now = datetime.now().time()
    start = time(22, 30)
    end = time(5, 0)

    return now >= start or now <= end


def timestamp():
    return datetime.now().strftime("%m-%d-%Y %H:%M")


class AutoRune:
    def __init__(self):
        self.rl = RuneLiteWindow()
        self.rl.activate()
        sleep(0.5)

        self.login = LoginLogout(self.rl)

        self.bh = BirdhouseRun(self.rl)
        self.last_bh = TrackTask("birdhouse_run")

        self.craft = MoltenGlass(self.rl)

    def initialize_player(self) -> int | None:
        response = get_player_by_name(self.rl.player_name)

        if response.status_code == 404:
            player = create_player(self.rl.player_name)
            return player.json()["id"]

        if response.status_code == 200:
            return response.json()["id"]

        return None

    def sleep_timer(self):
        sleep_time = random_interval() - self.last_bh.time_since_task()
        sleep_time = sleep_time if sleep_time > 0 else 1

        print(f"{timestamp()}: Sleeping for {sleep_time} minutes.")

        return sleep_time * 60

    def do_birdhouse_run(self, player_id: int) -> bool:
        self.login.login_now()

        bird_nests = self.bh.main()

        print(f"{timestamp()}: Completed birdhouse run")

        payload = Run(
            account_id=player_id,
            bird_nests=bird_nests,
        )

        return submit_bird_run(payload).status_code == 200

    def main(self):
        do_crafting = True

        player_id = self.initialize_player()

        while True:
            if bedtime():
                sleep(3600)
                continue

            if self.last_bh.time_since_task() > 50:
                if not self.do_birdhouse_run(player_id):
                    break

                if do_crafting and not self.craft.main():
                    do_crafting = False

                sleep(300)
                self.login.logout_now()
                print(f"{timestamp()}: Logged out successfully")

            sleep(self.sleep_timer())


if __name__ == "__main__":
    print(f"{timestamp()}: Started Script")
    play = AutoRune()
    play.main()
