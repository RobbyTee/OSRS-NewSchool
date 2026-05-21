import requests


def get_player_stats() -> dict:
    stats_request = requests.get(url="http://127.0.0.1:8080/stats", timeout=5)
    stats = {}
    for query in stats_request.json():
        stat_name = query["stat"]
        stat_level = query["level"]
        stats[stat_name.lower()] = stat_level

    return stats


def stat_level(stat: str):
    stat = stat.lower()
    player_stats = get_player_stats()
    return player_stats[stat]
