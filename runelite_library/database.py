from dataclasses import asdict

import requests

from config import settings
from custom_dataclasses import Account, BirdhouseRun

DATABASE_URL = settings.db_url


class NullDatabase:
    def create_player(*args, **kwargs) -> int:
        return 200

    def get_player_by_name(*args, **kwargs) -> int:
        return 200

    def patch_player_stats(*args, **kwargs) -> int:
        return 200

    def submit_bird_run(*args, **kwargs) -> int:
        return 200

    def test_database_connection(*args, **kwargs) -> int:
        return 200


class RuneDashboard:
    def create_player(self, account_name: str) -> requests.Response:
        payload = {"account_name": account_name}
        endpoint = "/api/accounts"
        url = DATABASE_URL + endpoint

        return requests.post(
            url,
            json=payload,
            timeout=5,
        )

    def get_player_by_name(self, account_name: str) -> requests.Response:
        endpoint = f"/api/accounts/name/{account_name}"
        url = DATABASE_URL + endpoint

        return requests.get(
            url,
            timeout=5,
        )

    def patch_player_stats(
        self,
        account: Account,
        account_id: int,
    ) -> requests.Response:
        endpoint = f"/api/accounts/id/{account_id}"
        url = DATABASE_URL + endpoint

        payload = {
            field: value
            for field, value in asdict(account).items()
            if value is not None
        }

        return requests.patch(
            url,
            json=payload,
            timeout=5,
        )

    def submit_bird_run(self, birdhouse_run: BirdhouseRun) -> requests.Response:
        endpoint = "/api/runs"
        url = DATABASE_URL + endpoint

        return requests.post(
            url,
            json=asdict(birdhouse_run),
            timeout=5,
        )

    def test_database_connection(self) -> requests.status_codes:
        endpoint = "/api/servers"
        url = DATABASE_URL + endpoint

        return requests.get(url, timeout=5).status_code
