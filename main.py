import random
from datetime import datetime, time
from time import sleep

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

        self.last_bh = TrackTask("birdhouse_run")

        self.craft = MoltenGlass(self.rl)

    def sleep_timer(self):
        sleep_time = random_interval() - self.last_bh.time_since_task()
        sleep_time = sleep_time if sleep_time > 0 else 1

        print(f"{timestamp()}: Sleeping for {sleep_time} minutes.")

        return sleep_time * 60

    def do_birdhouse_run(self):

        return

    def main(self):
        do_crafting = True

        self.bh = BirdhouseRun(self.rl)

        while True:
            if bedtime():
                sleep(3600)
                continue

            if self.last_bh.time_since_task() > 50:
                self.login.login_now()
                if not self.bh.main():
                    break

                print(f"{timestamp()}: Completed birdhouse run")

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
