from enum import Enum, auto
from time import sleep, time

from runelite_library.bank import Bank
from runelite_library.interact import RuneliteComponent, close_interface, press
from runelite_library.player import Player
from runelite_library.rune_logger import log_event
from too_many_items import (
    BankObjects,
    ItemObjects,
    ToolObjects,
)

BANK_TAB = BankObjects.tab_ii
TIME_TO_CRAFT = 15  # in minutes (or 0 to disable)

GLASS_REQS = {
    "Beer Glass": {
        "level": 1,
        "option": "1",
    },
    "Candle Lantern": {
        "level": 4,
        "option": "2",
    },
    "Oil Lamp": {
        "level": 12,
        "option": "3",
    },
    "Vial": {
        "level": 33,
        "option": "4",
    },
    "Fishbowl": {
        "level": 42,
        "option": "5",
    },
    "Glass Orb": {
        "level": 46,
        "option": "6",
    },
    "Bullseye Lantern Lens": {
        "level": 49,
        "option": "7",
    },
    "Dorgeshuun Light Orb": {
        "level": 87,
        "option": "8",
    },
}


class GlassBlowingStates(Enum):
    INIT = auto()
    GEAR_PREP = auto()
    OPEN_BANK = auto()
    WITHDRAW_GEAR = auto()
    RETURN_TO_BANK = auto()
    CRAFT = auto()
    COMPLETE = auto()
    FAILURE = auto()


class MoltenGlass(RuneliteComponent):
    def glassblowing(self, state):
        while True:
            if state == GlassBlowingStates.INIT:
                log_event(f"Starting {__name__}")
                p = Player(self.rl)
                p_crafting_level = p.stat_level("crafting")

                for craft_method, reqs in GLASS_REQS.items():
                    if reqs["level"] <= p_crafting_level:
                        craft_option = reqs["option"]
                        to_craft = craft_method

                log_event(
                    f"Player's crafting level is {p_crafting_level}, crafting {to_craft}"
                )

                state = GlassBlowingStates.GEAR_PREP

            elif state == GlassBlowingStates.GEAR_PREP:
                tools = [ToolObjects.glassblowing_pipe]
                resource = [ItemObjects.molten_glass]

                state = GlassBlowingStates.OPEN_BANK

            elif state == GlassBlowingStates.OPEN_BANK:
                bank = Bank(self.rl)
                if not bank.open_bank():
                    state = GlassBlowingStates.RETURN_TO_BANK
                    continue

                state = GlassBlowingStates.WITHDRAW_GEAR

            elif state == GlassBlowingStates.WITHDRAW_GEAR:
                bank.deposit_inventory()
                bank.open_tab(BANK_TAB)
                bank.withdraw(tools)
                try:
                    bank.withdraw(
                        resource,
                        "all",
                        check_quantity=True,
                    )
                except TimeoutError as e:
                    log_event(
                        f"Missing necessary ingredients for {__name__}\n {e}",
                        "error",
                    )
                    close_interface()
                    state = GlassBlowingStates.FAILURE
                    continue
                close_interface()
                state = GlassBlowingStates.CRAFT

            elif state == GlassBlowingStates.CRAFT:
                self.inventory.click(ToolObjects.glassblowing_pipe)
                self.inventory.click(ItemObjects.molten_glass)
                sleep(0.5)
                press(craft_option)
                sleep(50)
                state = GlassBlowingStates.COMPLETE

            elif state == GlassBlowingStates.COMPLETE:
                log_event(f"{__name__} completed successfully\n")
                return True

            elif state == GlassBlowingStates.FAILURE:
                log_event(f"{__name__} experienced a failure\n", "error")
                return False

            elif state == GlassBlowingStates.RETURN_TO_BANK:
                log_event(f"{__name__} found no bank\n", "error")
                if bank.return_to_bank():
                    state = GlassBlowingStates.OPEN_BANK
                    continue

                state = GlassBlowingStates.FAILURE

    def main(self, state=GlassBlowingStates.INIT):
        start_time = time()

        while True:
            still_crafting = bool(time() - start_time <= (TIME_TO_CRAFT * 60))
            if not still_crafting:
                return True

            if still_crafting and self.glassblowing(state):
                continue

            return False
