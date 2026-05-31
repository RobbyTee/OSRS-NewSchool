# Use this for debugging as needed

from runelite_library.database import (
    Account,
    BirdhouseRun,
    create_player,
    get_player_by_name,
    submit_bird_run,
    update_player_stats,
)
from runelite_library.interact import Interact
from runelite_library.window_management import RuneLiteWindow
from too_many_items import ItemObjects

rl = RuneLiteWindow()
i = Interact(rl)

seed_nest = i.count_object(ItemObjects.seed_nest)
nest = i.count_object(ItemObjects.empty_birdnest)
ring_nest = i.count_object(ItemObjects.ring_nest)
total = seed_nest + nest + ring_nest

print(f"Seeds = {seed_nest}")
print(f"Rings = {ring_nest}")
print(f"Empty = {nest}")
print(f"Total = {total}")

# create_player("Elven Steve")
# if r.status_code == 409:
#         print(f"Player is already in database: {account_name}")
#         return True

#     if r.status_code == 200:
#         print(f"Added player to database: {account_name}")
#         return True

#     print(
#         f"Failed to create player {account_name} with status: {r.status_code}\n\n{r.text}"
#     )
#     return False


#### PATCH ####

# name = "Elven Steve"

# account_id = get_player_by_name(name).json()["id"]

# account = Account(
#     account_name=name,
#     strength_level=20,
#     crafting_level=40,
# )

# print(update_player_stats(account, account_id).json())

## Submit Run ##
# birdhouse_run = BirdhouseRun(
#     account_id=4,
#     bird_nests=5,
# )

# print(submit_bird_run(birdhouse_run).status_code)
