from dataclasses import asdict, dataclass

import requests

DATABASE_URL = "http://webserver.spareroom.com:8000"


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


@dataclass
class BirdhouseRun:
    account_id: int
    bird_nests: int


def create_player(account_name: str) -> requests.Response:
    payload = {"account_name": account_name}
    endpoint = "/api/accounts"
    url = DATABASE_URL + endpoint

    return requests.post(
        url,
        json=payload,
        timeout=5,
    )


def get_player_by_name(account_name: str) -> requests.Response:
    endpoint = f"/api/accounts/name/{account_name}"
    url = DATABASE_URL + endpoint

    return requests.get(
        url,
        timeout=5,
    )


def update_player_stats(
    account: Account,
    account_id: int,
) -> requests.Response:
    endpoint = f"/api/accounts/id/{account_id}"
    url = DATABASE_URL + endpoint

    payload = {
        field: value for field, value in asdict(account).items() if value is not None
    }

    return requests.patch(
        url,
        json=payload,
        timeout=5,
    )


def submit_bird_run(birdhouse_run: BirdhouseRun) -> requests.Response:
    endpoint = "/api/runs"
    url = DATABASE_URL + endpoint

    return requests.post(
        url,
        json=asdict(birdhouse_run),
        timeout=5,
    )
