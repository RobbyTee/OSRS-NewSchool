from datetime import datetime, timezone
from pathlib import Path

LOG_DIRECTORY = "./utils"


def get_current_utc_date():
    return datetime.now(timezone.utc)


class TrackLog:
    def __init__(self, log_file: str):
        self.log_dir = Path(LOG_DIRECTORY)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = log_file + ".log"
        self.log_path = self.log_dir / self.log_file

        if not self.log_path.exists():
            self.initialize()

    def read(self):
        """Returns the entire log file"""
        with self.log_path.open() as file:
            return file.read()

    def initialize(self):
        """Creates a blank log file"""
        self.log_path.touch()

    def reset(self):
        with self.log_path.open("w") as file:
            file.write("")

    def append_datetime(self):
        """Appends log file with current timestamp"""
        with self.log_path.open("a") as file:
            file.write(f"{self.timestamp()}\n")

    def overwrite_datetime(self):
        """Overwrites log file with current timestamp"""
        with self.log_path.open("w") as file:
            file.write(f"{self.timestamp()}\n")

    @staticmethod
    def timestamp():
        """Returns current date and time"""
        now = get_current_utc_date()
        return now.isoformat()

    def time_since_last_logged(self) -> int:
        """Returns time in minutes from last timestamp"""
        timestamps = self.read()

        if not timestamps:
            return 999

        last_timestamp_str = timestamps.splitlines()[-1]

        last_timestamp = datetime.fromisoformat(
            last_timestamp_str,
        ).replace(
            tzinfo=timezone.utc,
        )

        now = get_current_utc_date()

        return int((now - last_timestamp).total_seconds() / 60)
