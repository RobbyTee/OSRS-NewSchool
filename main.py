from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun

rl = RuneLiteWindow()
rl.activate()
sleep(0.5)

login = LoginLogout(rl)
login.login_now()

b = BirdhouseRun(rl)
print(b.main())
