from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.tracker import TrackTask
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun

rl = RuneLiteWindow()
rl.activate()
sleep(0.5)

login = LoginLogout(rl)

bh = BirdhouseRun(rl)
last_bh = TrackTask("birdhouse_run")

do_task = False

# print(last_bh.time_since_task())

while True:
    if last_bh.time_since_task() > 50:
        do_task = True

    if do_task:
        login.login_now()

        if bh.main():
            sleep(240)
            login.logout_now()
            do_task = False
        else:
            break

    sleep(60)
