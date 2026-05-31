from dataclasses import asdict

import requests

from config import settings
from custom_dataclasses import Account, BirdhouseRun

# DATABASE_URL = "http://webserver.spareroom.com:8000"
DATABASE_URL = settings.db_url


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


def test_database_connection() -> requests.status_codes:
    endpoint = "/api/servers"
    url = DATABASE_URL + endpoint

    return requests.get(url, timeout=5).status_code


class DatabaseCalls:
    def __init__(self):
        pass
