from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.player import Player
from runelite_library.rune_logger import log_event
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun, State
from too_many_items import MiscObjects, PathingObjects

rl = RuneLiteWindow()
rl.activate()
sleep(0.5)

login = LoginLogout(rl)
login.login_now()

b = BirdhouseRun(rl)
print(b.main())
