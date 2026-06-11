from runelite_library.interact import Interact
from runelite_library.login import LoginLogout
from runelite_library.player import Player
from runelite_library.window_management import RuneLiteWindow
from tasks.mort_myre_fungus import MortMyreFungus, State
from too_many_items import GlobalColorObjects, WearableObjects

rl = RuneLiteWindow()
rl.activate()

# login = LoginLogout(rl)
# login.login_now()

m = MortMyreFungus(rl)
m.state_machine()
