from enum import Enum, auto
from time import sleep, time

from runelite_library.bank import Bank
from runelite_library.interact import RuneliteComponent, close_interface, press
from runelite_library.player import Player
from runelite_library.rune_logger import log_event
from too_many_items import (
    BankObjects,
    GlobalColorObjects,
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
                return 0

            elif state == GlassBlowingStates.FAILURE:
                log_event(f"{__name__} experienced a failure\n", "error")
                return 1

            elif state == GlassBlowingStates.RETURN_TO_BANK:
                log_event(f"{__name__} found no bank\n", "error")
                return 2

    def main(self, state=GlassBlowingStates.INIT):
        start_time = time()

        while True:
            if time() - start_time <= (TIME_TO_CRAFT * 60):
                result = self.glassblowing(state)

                if result == 2:
                    return False

                if result == 1:
                    return False

            else:
                return True


class NecklaceStates(Enum):
    INIT = auto()
    GEAR_PREP = auto()
    OPEN_BANK = auto()
    WITHDRAW_GEAR = auto()


class RubyNecklace(RuneliteComponent):
    def player_in_edgeville(self) -> bool:
        return bool(self.client.find_by_image(BankObjects.edgeville))

    def state_machine(self, state):
        if state == NecklaceStates.INIT:
            teleport_to_edgeville = True

            p = Player(self.rl)

            if self.player_in_edgeville():
                teleport_to_edgeville = False

            if p.stat_level("crafting") < 40:
                raise ValueError(
                    f"Your crafting level is not greater than 40: got {p.stat_level('crafting')}"
                )

    def main(self, state=NecklaceStates.INIT):
        return self.state_machine(state)
