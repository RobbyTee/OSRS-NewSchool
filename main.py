from time import sleep

from runelite_library.interact import Bank, LoginLogout, close_interface
from runelite_library.rune_logger import log_event
from runelite_library.teleports import Spells, Wearable
from runelite_library.window_management import RuneLiteWindow
from too_many_items import BankObjects, RuneObjects, WearableObjects

log_event(f"{__name__} started")

rl = RuneLiteWindow()
rl.activate()
sleep(0.5)

bank = Bank(rl)
login = LoginLogout(rl)
inv_jewelry = Wearable(rl)
eq_jewelry = Wearable(rl, True)
spell = Spells(rl)

login.login_now()

bank.open_bank()
# bank.deposit_equipment()
bank.deposit_inventory()

bank.open_tab(BankObjects.tab_all)
items_to_withdraw = [
    WearableObjects.amulet_of_glory,
]
bank.withdraw(items_to_withdraw)

bank.open_tab(BankObjects.tab_i)
runes_to_withdraw = [
    RuneObjects.air,
    RuneObjects.fire,
    RuneObjects.mind,
]
bank.withdraw(runes_to_withdraw, "all")

close_interface()

inv_jewelry.amulet_of_glory("draynor_village")
inv_jewelry.teleport(
    wearable="amulet_of_glory",
    location="draynor_village",
)

# spell.normal_spellbook("home")
