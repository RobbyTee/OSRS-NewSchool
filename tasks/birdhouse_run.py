from enum import Enum, auto
from time import sleep

from config import settings
from custom_dataclasses import BirdhouseRun as Run
from runelite_library.bank import Bank
from runelite_library.database import NullDatabase, RuneDashboard
from runelite_library.interact import RuneliteComponent, close_interface
from runelite_library.player import Player
from runelite_library.rune_logger import log_event
from runelite_library.teleports import Wearable
from runelite_library.tracker import TrackLog
from too_many_items import (
    BankObjects,
    GlobalColorObjects,
    ItemObjects,
    MenuObjects,
    MiscObjects,
    ToolObjects,
    ToolTips,
    WearableObjects,
)

DATABASE = RuneDashboard if settings.use_database else NullDatabase

SEED_TYPE = settings.seed_type.value
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

BIRDHOUSES = {
    1: MiscObjects.bh1,
    2: MiscObjects.bh2,
    3: MiscObjects.bh3,
    4: MiscObjects.bh4,
}


class State(Enum):
    INIT = auto()
    GEAR_PREP = auto()
    OPEN_BANK = auto()
    WITHDRAW_GEAR = auto()
    EQUIP_GEAR = auto()
    CLICK_BH = auto()
    CRAFT_BH = auto()
    FILL_BH = auto()
    GO_TO_NEXT_BH = auto()
    GO_TO_BANK = auto()
    COMPLETE = auto()
    FAILURE = auto()
    RETURN_TO_BANK = auto()


class BirdhouseRun(RuneliteComponent):
    def __init__(self, rl):
        super().__init__(rl)
        self.p = Player(self.rl)
        self.account_id = self.p.get_player_id()

        self.d = DATABASE()

    def go_to_bh_1(self):
        dp = Wearable(self.rl)
        dp.teleport("digsite_pendant", "fossil_island")

        try:
            self.play_window.click(
                GlobalColorObjects.mush_tree,
                timeout=5,
            )
        except TimeoutError:
            self.p.step_to(1)
            return False

        self.play_window.click(MenuObjects.verdant_valley)
        return True

    def go_to_bh_2(self):
        self.p.step_to(1)
        sleep(4)

    def go_to_bh_3(self):
        try:
            self.play_window.click(
                GlobalColorObjects.mush_tree,
                timeout=5,
            )
        except TimeoutError:
            self.p.step_to(2)
            return False

        self.play_window.click(MenuObjects.mushroom_meadow)
        self.p.step_to(10)
        sleep(5)
        return True

    def go_to_bh_4(self):
        self.p.path_to(6)
        sleep(5)

    def state_machine(self, state):
        bh_step = 1
        bh_crafted = False

        while True:
            if state == State.INIT:
                hunter_level = self.p.stat_level("hunter")
                crafting_level = self.p.stat_level("crafting")

                log_type = ItemObjects.logs
                for reqs in birdhouse_reqs.values():
                    # print(f"{birdhouse}= crafting, {reqs['log']}")
                    if (
                        reqs["hunter"] <= hunter_level
                        and reqs["crafting"] <= crafting_level
                    ):
                        log_type = reqs["log"]

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
                if self.p.stat_level("hunter") >= 24:
                    equipment.append(WearableObjects.rabbits_foot)
                    equip_rabbits_foot = True

                logs = [log_type] * 4
                seeds = [SEED_TYPE] * 4

                state = State.OPEN_BANK

            elif state == State.OPEN_BANK:
                bank = Bank(self.rl)
                if not bank.open_bank():
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
                try:
                    bank.open_tab(BankObjects.tab_iii)
                    bank.withdraw(tools)
                    bank.withdraw(equipment, check_quantity=True)
                    bank.withdraw(logs, check_quantity=True)
                    bank.withdraw(seeds, 10, check_quantity=True)
                except TimeoutError as e:
                    log_event(
                        f"Missing necessary ingredients for {__name__}\n {e}",
                        "error",
                    )
                    close_interface()
                    state = State.FAILURE
                    continue
                close_interface()
                log_event(f"Done withdrawing gear for {__name__}")
                state = State.EQUIP_GEAR

            elif state == State.EQUIP_GEAR:
                if equip_rabbits_foot:
                    log_event("Equipping rabbits foot", "debug")
                    self.inventory.click(WearableObjects.rabbits_foot)
                state = State.GO_TO_NEXT_BH

            elif state == State.CLICK_BH:
                sleep(1)
                if not self.play_window.click(BIRDHOUSES.get(bh_step)):
                    state = State.FAILURE
                    continue

                if not bh_crafted:
                    state = State.CRAFT_BH
                    continue

                state = State.FILL_BH

            elif state == State.CRAFT_BH:
                try:
                    self.inventory.click(ItemObjects.clockwork)
                except TimeoutError:
                    state = State.CLICK_BH
                    continue

                self.inventory.click(log_type)  # From State.INIT
                sleep(1)
                bh_crafted = True
                state = State.CLICK_BH

            elif state == State.FILL_BH:
                self.inventory.click(SEED_TYPE)
                if not self.client.click(
                    BIRDHOUSES.get(bh_step),
                    mouse_tooltip=ToolTips.birdhouse_empty,
                ):
                    state = State.FAILURE
                    continue
                if bh_step == 4:
                    state = State.GO_TO_BANK
                    continue

                bh_crafted = False
                bh_step += 1
                state = State.GO_TO_NEXT_BH

            elif state == State.GO_TO_NEXT_BH:
                if bh_step == 1:
                    if not self.go_to_bh_1():
                        continue
                elif bh_step == 2:
                    self.go_to_bh_2()
                elif bh_step == 3:
                    if not self.go_to_bh_3():
                        continue
                else:
                    self.go_to_bh_4()
                state = State.CLICK_BH

            elif state == State.GO_TO_BANK:
                self.p.path_to(7)
                sleep(5)
                state = State.COMPLETE

            elif state == State.COMPLETE:
                bh_run = TrackLog("birdhouse_run")
                bh_run.overwrite_datetime()

                empty_nest = self.inventory.count_object(ItemObjects.empty_birdnest)
                ring_nest = self.inventory.count_object(ItemObjects.ring_nest)
                seed_nest = self.inventory.count_object(ItemObjects.seed_nest)
                total_nests = empty_nest + ring_nest + seed_nest

                payload = Run(
                    account_id=self.account_id,
                    bird_nests=total_nests,
                )

                response_code = self.d.submit_bird_run(payload).status_code
                if response_code != 200:
                    log_event(
                        f"Uploading birhouse run data to database failed with status code: {response_code}",
                        "error",
                    )

                self.p.update_player_stats(
                    account_name=self.rl.player_name,
                    account_id=self.account_id,
                )

                log_event(f"{__name__} completed successfully\n")
                return True

            elif state == State.FAILURE:
                log_event(f"{__name__} experienced a failure\n", "error")
                return False

            elif state == State.RETURN_TO_BANK:
                log_event(f"{__name__} found no bank\n", "error")
                if bank.return_to_bank():
                    state = State.OPEN_BANK
                    continue

                state = State.FAILURE

    def main(self, state=State.INIT):
        log_event(f"Starting {__name__}")
        return self.state_machine(state)
