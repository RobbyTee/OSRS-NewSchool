import random
from datetime import datetime, time
from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.tracker import TrackTask
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun


def random_interval():
    return random.uniform(50, 75)


def bedtime():
    now = datetime.now().time()
    start = time(20, 0)
    end = time(5, 0)

    return now >= start or now <= end


def main():
    rl = RuneLiteWindow()
    rl.activate()
    sleep(0.5)

    login = LoginLogout(rl)

    bh = BirdhouseRun(rl)
    last_bh = TrackTask("birdhouse_run")

    do_task = False

    while True:
        if bedtime():
            sleep(3600)

        if last_bh.time_since_task() > 50:
            do_task = True

        if do_task:
            login.login_now()

            if bh.main():
                sleep(30)
                login.logout_now()
                do_task = False
            else:
                break

        sleep(random_interval() * 60)


if __name__ == "__main__":
    main()
