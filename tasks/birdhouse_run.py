import json
from enum import Enum, auto
from pathlib import Path

from runelite_library.interact import Bank, RuneliteComponent, close_interface
from runelite_library.player import stat_level
from runelite_library.rune_logger import log_event
from too_many_items import (
    BankObjects,
    ItemObjects,
    ToolObjects,
    WearableObjects,
)

CONFIG_FILE = Path("config.json")
with Path.open(CONFIG_FILE) as file:
    CONFIG = json.load(file)

BIRDHOUSE_CONFIG = CONFIG["Birdhouse_Run"]
SEED_TYPE = BIRDHOUSE_CONFIG["seed_type"]
try:
    SEED_TYPE = getattr(ItemObjects, SEED_TYPE)
except AttributeError:
    raise KeyError(f"Item '{SEED_TYPE}' does not exist in ItemObjects.")


birdhouse_reqs = {
    "normal": {
        "hunter": 5,
        "crafting": 5,
        "log": ItemObjects.logs,
    },
    "oak": {
        "hunter": 14,
        "crafting": 15,
        "log": ItemObjects.oak_logs,
    },
    "willow": {
        "hunter": 24,
        "crafting": 25,
        "log": ItemObjects.willow_logs,
    },
    "teak": {
        "hunter": 34,
        "crafting": 35,
        "log": ItemObjects.teak_logs,
    },
    "maple": {
        "hunter": 44,
        "crafting": 45,
        "log": ItemObjects.maple_logs,
    },
    "mahogany": {
        "hunter": 49,
        "crafting": 50,
        "log": ItemObjects.mahogany_logs,
    },
    "yew": {
        "hunter": 59,
        "crafting": 60,
        "log": ItemObjects.yew_logs,
    },
    "magic": {
        "hunter": 74,
        "crafting": 75,
        "log": ItemObjects.magic_logs,
    },
    "redwood": {
        "hunter": 89,
        "crafting": 90,
        "log": ItemObjects.redwood_logs,
    },
}


class State(Enum):
    INIT = auto()
    GEAR_PREP = auto()
    OPEN_BANK = auto()
    WITHDRAW_GEAR = auto()
    EQUIP_GEAR = auto()
    COMPLETE = auto()
    FAILURE = auto()
    RETURN_TO_BANK = auto()


class BirdhouseRun(RuneliteComponent):
    def state_machine(self, state=State.INIT):
        while True:
            if state == State.INIT:
                hunter_level = stat_level("hunter")
                crafting_level = stat_level("crafting")

                log_type = ItemObjects.logs
                for reqs in birdhouse_reqs.values():
                    # print(f"{birdhouse}= crafting, {reqs['log']}")
                    log_type = (
                        reqs["log"]
                        if reqs["hunter"] <= hunter_level
                        and reqs["crafting"] <= crafting_level
                        else ItemObjects.logs
                    )

                log_event(
                    f"Chose {log_type} based on player's hunter ({hunter_level}) and crafting ({crafting_level}) levels.",
                )

                state = State.GEAR_PREP

            elif state == State.GEAR_PREP:
                tools = [
                    ToolObjects.hammer,
                    ToolObjects.chisel,
                ]

                equipment = [WearableObjects.digsite_pendant]

                equip_rabbits_foot = False
                if stat_level("hunter") >= 24:
                    equipment.append(WearableObjects.rabbits_foot)
                    equip_rabbits_foot = True

                logs = [log_type] * 4
                seeds = [SEED_TYPE] * 4

                state = State.OPEN_BANK

            elif state == State.OPEN_BANK:
                bank = Bank(self.rl)
                if not bank.open_bank("bank_chest"):
                    state = State.RETURN_TO_BANK
                    continue

                state = State.WITHDRAW_GEAR

            elif state == State.WITHDRAW_GEAR:
                log_event(
                    f"Attempting to withdraw:\n{tools}\n{equipment}\n{logs}\n{seeds}",
                    level="debug",
                )
                bank.deposit_equipment()
                bank.deposit_inventory()
                bank.open_tab(BankObjects.tab_iii)
                bank.withdraw(tools)
                bank.withdraw(equipment)
                bank.withdraw(logs, check_quantity=True)
                bank.withdraw(seeds, 10, check_quantity=True)
                close_interface()
                log_event("Done withdrawing gear for birdhouse run")
                state = State.EQUIP_GEAR

            elif state == State.EQUIP_GEAR:
                if equip_rabbits_foot:
                    log_event("Equipping rabbits foot", "debug")
                    self.inventory.click(WearableObjects.rabbits_foot)
                state = State.COMPLETE

            elif state == State.COMPLETE:
                log_event(f"{__name__} completed successfully\n")
                return 0

            elif state == State.FAILURE:
                log_event(f"{__name__} experienced a failure\n", "error")
                return 1

            elif state == State.RETURN_TO_BANK:
                log_event(f"{__name__} found no bank\n", "error")
                return 2

    def main(self):
        log_event(f"Starting {__name__}")
        while True:
            result = self.state_machine()
            if result == 2:
                Bank.return_to_bank()
            elif result == 1:
                return False
            elif result == 0:
                return True
