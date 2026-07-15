import random
from datetime import datetime, time
from enum import Enum, auto
from time import sleep

from runelite_library.login import LoginLogout
from runelite_library.tracker import TrackLog
from runelite_library.window_management import RuneLiteWindow
from tasks.birdhouse_run import BirdhouseRun
from tasks.crafting import MoltenGlass
from tasks.mort_myre_fungus import MortMyreFungus

TOTAL_MM_RUNS = 6  # How many money maker runs?


def random_interval():
    return int(random.uniform(50, 60))


def bedtime():
    now = datetime.now().time()
    start = time(24, 0)
    end = time(5, 0)

    return now >= start or now <= end


def timestamp():
    return datetime.now().strftime("%m-%d-%Y %H:%M")


class State(Enum):
    INIT = auto()
    BEDTIME = auto()
    CHOOSE_TASK = auto()
    HUNTER = auto()
    CRAFTING = auto()
    MONEY_MAKER = auto()
    REST_UNTIL_HUNTER = auto()
    COMPLETE = auto()
    FAILURE = auto()


class AutoRune:
    def __init__(self):
        self.rl = RuneLiteWindow()
        self.rl.activate()
        sleep(0.5)

        self.login = LoginLogout(self.rl)

        self.last_bh = TrackLog("birdhouse_run")

        self.craft = MoltenGlass(self.rl)

        self.fungus = MortMyreFungus(self.rl)

    def sleep_timer(self):
        sleep_time = random_interval() - self.last_bh.time_since_last_logged()
        sleep_time = sleep_time if sleep_time > 0 else 1

        print(f"{timestamp()}: Sleeping for {sleep_time} minutes.")

        return sleep_time * 60

    def state_machine(self, state=State.INIT):
        crafting = True
        collect_fungi = True
        money_maker_runs = 0

        while True:
            if state == State.INIT:
                state = State.BEDTIME if bedtime() else State.CHOOSE_TASK

            elif state == State.BEDTIME:
                sleep(3600)
                state = State.INIT

            elif state == State.CHOOSE_TASK:
                if self.last_bh.time_since_last_logged() > 50:
                    state = State.HUNTER
                    continue

                state = State.MONEY_MAKER

            elif state == State.HUNTER:
                money_maker_runs = 0

                self.login.login_now()

                self.bh = BirdhouseRun(self.rl)

                if not self.bh.main():
                    state == State.FAILURE
                    continue

                print(f"{timestamp()}: Completed birdhouse run")
                state = State.CRAFTING

            elif state == State.CRAFTING:
                if crafting and not self.craft.main():
                    print(f"{timestamp()}: No crafting supplies - disabled crafting")
                    crafting = False
                print(f"{timestamp()}: Completed crafting task")
                state = State.INIT

            elif state == State.MONEY_MAKER:
                if money_maker_runs >= TOTAL_MM_RUNS:
                    print(f"{timestamp()}: Maxed out money maker runs. Resting!")
                    state = State.REST_UNTIL_HUNTER
                    continue

                self.login.login_now()
                if collect_fungi and not self.fungus.main():
                    state = State.REST_UNTIL_HUNTER
                    continue

                money_maker_runs += 1
                print(
                    f"{timestamp()}: Completed money maker run ({TOTAL_MM_RUNS - money_maker_runs} more runs left)"
                )
                state = State.INIT

            elif state == State.REST_UNTIL_HUNTER:
                sleep(self.sleep_timer())
                state = State.INIT


if __name__ == "__main__":
    print(f"{timestamp()}: Started Script")
    play = AutoRune()
    play.state_machine()
