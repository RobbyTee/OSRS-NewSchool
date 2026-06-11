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
    Food,
    GlobalColorObjects,
    ItemObjects,
    MenuObjects,
    MiscObjects,
    ToolObjects,
    ToolTips,
    WearableObjects,
)

FOOD_SOURCE = Food.lobster
BANK_TAB = BankObjects.tab_vi


class State(Enum):
    INIT = auto()
    PREPARE_GEAR = auto()
    OPEN_BANK = auto()
    WITHDRAW_GEAR = auto()
    EQUIP_GEAR = auto()
    TELEPORT_TO_MONASTERY = auto()
    RECHARGE_PRAYER = auto()
    PATH_TO_FAIRY_RING = auto()
    USE_FAIRY_RING = auto()
    OPEN_SWAMP_GATE = auto()
    PATH_TO_LOGS = auto()
    CHECK_HEALTH = auto()
    CHECK_PRAYER = auto()
    CHECK_INVENTORY = auto()
    FARM_FUNGUS = auto()
    TELEPORT_TO_CASTLE_WARS = auto()
    COMPLETE = auto()
    FAILURE = auto()
    RETURN_TO_BANK = auto()


class MortMyreFungus(RuneliteComponent):
    def state_machine(self, state=State.INIT):
        while True:
            if state == State.INIT:
                player = Player(self.rl)

                state = State.PREPARE_GEAR

            elif state == State.PREPARE_GEAR:
                withdraw_food = False

                if player.health < 30:
                    withdraw_food = True

                state = State.OPEN_BANK

            elif state == State.OPEN_BANK:
                bank = Bank(self.rl)
                if not bank.open_bank():
                    state = State.RETURN_TO_BANK
                    continue

                bank.deposit_equipment()
                bank.deposit_inventory()

                state = State.WITHDRAW_GEAR

            elif state == State.WITHDRAW_GEAR:
                equippables = [
                    WearableObjects.ardougne_cloak,
                    WearableObjects.ring_of_dueling,
                    WearableObjects.dramen_staff,
                ]

                items = [ItemObjects.sickle]

                if withdraw_food:
                    items.append(FOOD_SOURCE)

                bank.open_tab(BANK_TAB)
                bank.withdraw(equippables)
                bank.withdraw(items)

                close_interface()

                if withdraw_food:
                    self.inventory.click(FOOD_SOURCE)

                state = State.EQUIP_GEAR

            elif state == State.EQUIP_GEAR:
                self.inventory.click(WearableObjects.ardougne_cloak)
                self.inventory.click(WearableObjects.ring_of_dueling)
                self.inventory.click(WearableObjects.dramen_staff)

                state = State.TELEPORT_TO_MONASTERY

            elif state == State.TELEPORT_TO_MONASTERY:
                cape = Wearable(self.rl, equipped=True)
                cape.teleport(
                    item="ardougne_cloak",
                    location="kandarin_monastery",
                )

                state = State.RECHARGE_PRAYER

            elif state == State.RECHARGE_PRAYER:
                player.step_to(10)

                sleep(6)

                self.play_window.click(GlobalColorObjects.altar)

                sleep(3)

                state = State.PATH_TO_FAIRY_RING

            elif state == State.PATH_TO_FAIRY_RING:
                player.path_to(6, rest=3)

                sleep(2)

                state = State.USE_FAIRY_RING

            elif state == State.USE_FAIRY_RING:
                self.play_window.click(
                    GlobalColorObjects.fairy_ring,
                    click_type="right",
                )

                self.client.click(MenuObjects.cks)

                sleep(5)

                attempt_at_gate = 0
                state = State.OPEN_SWAMP_GATE

            elif state == State.OPEN_SWAMP_GATE:
                player.step_to(1)

                sleep(5)

                self.play_window.click(GlobalColorObjects.gate)
                attempt_at_gate += 1

                if attempt_at_gate > 3:
                    state = State.FAILURE
                    continue

                state = State.PATH_TO_LOGS

            elif state == State.PATH_TO_LOGS:
                player.step_to(2)

                sleep(4)

                if not player.step_to(3):
                    state = State.OPEN_SWAMP_GATE
                    continue

                sleep(5)

                state = State.FARM_FUNGUS

            elif state == State.CHECK_HEALTH:
                if player.health < 30:
                    state = State.TELEPORT_TO_CASTLE_WARS
                    continue

                state = State.CHECK_PRAYER

            elif state == State.CHECK_PRAYER:
                if player.prayer < 10:
                    state = State.TELEPORT_TO_CASTLE_WARS
                    continue

                state = State.CHECK_INVENTORY

            elif state == State.CHECK_INVENTORY:
                if player.inventory_full:
                    state = State.TELEPORT_TO_CASTLE_WARS
                    continue

                state = State.FARM_FUNGUS

            elif state == State.FARM_FUNGUS:
                self.inventory.click(ItemObjects.sickle)

                sleep(2)

                try:
                    while True:
                        self.play_window.click(GlobalColorObjects.fungus, timeout=0.5)
                        sleep(0.8)
                except TimeoutError:
                    player.step_to(3)

                state = State.CHECK_HEALTH

            elif state == State.TELEPORT_TO_CASTLE_WARS:
                ring = Wearable(self.rl, equipped=True)
                ring.teleport(
                    item="ring_of_dueling",
                    location="castle_wars",
                )

                sleep(4)
                player.step_to(1)
                sleep(4)

                state = State.COMPLETE

            elif state == State.COMPLETE:
                return True

            elif state == State.FAILURE:
                return False

            elif state == State.RETURN_TO_BANK:
                if bank.return_to_bank():
                    state = State.OPEN_BANK
                    continue

                state = State.FAILURE
