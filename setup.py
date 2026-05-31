from pathlib import Path

from dotenv import set_key

from custom_dataclasses import FKeys, ReactionTime, SeedType

ENV_FILE = Path(".env")

DEFAULT_ENV_FILE = """# Database URL (e.g. http://server.example.com:8000)
USE_DATABASE = True
DB_URL = ""

# Birdhouse Run Settings
SEED_TYPE = ""

# Interface Shortcuts (e.g. f5)
INVENTORY = ""
STATS = ""
SPELLS = ""
EQUIPMENT = ""
QUESTS = ""
LOGOUT = ""
EMOTES = ""
PRAYER = ""
COMBAT = ""
GROUPING = ""

# User Settings
REACTION_TIME = ""
DEBUG = False
"""


def create_env_file() -> None:
    if not ENV_FILE.exists():
        ENV_FILE.write_text(DEFAULT_ENV_FILE)


def capture_settings() -> dict:
    settings = {}

    # Database settings
    settings
    if input("\nAre you using RuneDashboard? (yes/no): ").strip().lower() == "yes":
        settings["USE_DATABASE"] = True
        settings["DB_URL"] = (
            input("\nDatabase URL (e.g. http://server.domain.com:8000): ")
            .strip()
            .lower()
        )

    # Birdhouse Settings
    valid_seeds = [seed.value for seed in SeedType]
    while True:
        seed = (
            input(f"\nWhat seed will you use to fill birdhouses? {valid_seeds}: ")
            .strip()
            .lower()
        )

        if seed in valid_seeds:
            settings["SEED_TYPE"] = seed
            break

        print("\nInvalid seed type, try again.")

    # Reaction time
    valid_reactions = [reaction.value for reaction in ReactionTime]
    while True:
        reaction_time = (
            input(f"\nWhat reaction time would you like to use? {valid_reactions}: ")
            .strip()
            .lower()
        )

        if reaction_time in valid_reactions:
            settings["REACTION_TIME"] = reaction_time
            break

        print("\nInvalid reaction time, try again.")

    # Interface Shortcuts
    valid_fkeys = [fkey.value for fkey in FKeys]
    interfaces = {
        "inventory": "f1",
        "stats": "f2",
        "spells": "f6",
        "equipment": "f4",
        "quests": "f3",
        "logout": "f10",
        "emotes": "f11",
        "prayer": "f5",
        "combat": "f8",
        "grouping": "f7",
    }

    print("\nSetup F-Keys:")
    for interface, default in interfaces.items():
        while True:
            shortcut = (
                input(f"Choose the f-key shortcut for {interface} (default={default})")
                .strip()
                .lower()
            ) or default

            if shortcut in valid_fkeys:
                settings[interface.upper()] = shortcut
                break

            print("Invalid f-key, try again.")

    return settings


def write_user_settings_to_env(settings: dict) -> None:
    for key, value in settings.items():
        if not value:
            continue
        set_key(str(ENV_FILE), key, str(value))


def setup() -> None:
    create_env_file()

    user_settings = capture_settings()

    write_user_settings_to_env(user_settings)
    print("\nSettings saved to .env")


if __name__ == "__main__":
    setup()
