from dataclasses import dataclass
from enum import Enum


class ReactionTime(Enum):
    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"


@dataclass
class Account:
    account_name: str

    attack_level: int | None = None
    strength_level: int | None = None
    defence_level: int | None = None
    ranged_level: int | None = None
    prayer_level: int | None = None
    agility_level: int | None = None
    construction_level: int | None = None
    cooking_level: int | None = None
    crafting_level: int | None = None
    farming_level: int | None = None
    firemaking_level: int | None = None
    fishing_level: int | None = None
    fletching_level: int | None = None
    herblore_level: int | None = None
    hunter_level: int | None = None
    magic_level: int | None = None
    mining_level: int | None = None
    runecraft_level: int | None = None
    sailing_level: int | None = None
    slayer_level: int | None = None
    smithing_level: int | None = None
    thieving_level: int | None = None
    woodcutting_level: int | None = None
    hitpoints_level: int | None = None


@dataclass
class BirdhouseRun:
    account_id: int
    bird_nests: int


class SeedType(str, Enum):
    ONION_SEED = "onion_seed"


class FKeys(str, Enum):
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
