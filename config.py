from pydantic_settings import BaseSettings, SettingsConfigDict

from custom_dataclasses import SeedType


class Settings(BaseSettings):
    # Database Settings
    use_database: bool
    db_url: str

    # Birdhouse Settings
    seed_type: SeedType

    # Interface Shortcuts
    inventory: str
    stats: str
    spells: str
    equipment: str
    quests: str
    logout: str
    emotes: str
    prayer: str
    combat: str
    grouping: str

    # User Settings
    reaction_time: str
    debug: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
