import random
from datetime import datetime, time
from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.tracker import TrackTask
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun
from tasks.crafting import MoltenGlass

DO_CRAFTING = True


def random_interval():
    return int(random.uniform(50, 60))


def bedtime():
    now = datetime.now().time()
    start = time(20, 0)
    end = time(5, 0)

    return now >= start or now <= end


def timestamp():
    return datetime.now().strftime("%m-%d-%Y %H:%M")


class AutoRune:
    def __init__(self):
        rl = RuneLiteWindow()
        rl.activate()
        sleep(0.5)

        self.login = LoginLogout(rl)

        self.bh = BirdhouseRun(rl)
        self.last_bh = TrackTask("birdhouse_run")

        self.craft = MoltenGlass(rl)

    def sleep_timer(self):
        sleep_time = random_interval() - self.last_bh.time_since_task()
        sleep_time = sleep_time if sleep_time > 0 else 1

        print(f"{timestamp()}: Sleeping for {sleep_time} minutes.")

        return sleep_time * 60

    def main(self):
        do_task = False

        while True:
            if bedtime():
                sleep(3600)

            elif self.last_bh.time_since_task() > 50:
                do_task = True

            elif do_task:
                self.login.login_now()

                if self.bh.main():
                    print(f"{timestamp()}: Completed birdhouse run")
                    if DO_CRAFTING and not self.craft.main():
                        DO_CRAFTING = False

                    sleep(300)
                    self.login.logout_now()
                    print(f"{timestamp()}: Logged out successfully")
                    do_task = False

                else:
                    break

            sleep(self.sleep_timer())


if __name__ == "__main__":
    print(f"{timestamp()}: Started Script")
    play = AutoRune()
    play.main()
