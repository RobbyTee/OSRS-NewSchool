from runelite_library.bank import Bank
from runelite_library.interact import Interact
from runelite_library.player import Player
from runelite_library.window_management import RuneLiteWindow
from too_many_items import ItemObjects

rl = RuneLiteWindow()
i = Interact(rl)
b = Bank(rl)

p = Player(rl)
print(p.update_player_stats(account_name="Hellen Goose", account_id=4))
