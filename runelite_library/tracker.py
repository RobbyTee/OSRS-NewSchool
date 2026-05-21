from datetime import datetime, timedelta, timezone
from pathlib import Path


def get_current_utc_date():
    return datetime.now(timezone.utc)


class TrackItem:
    def __init__(self, item: str):
        self.log_dir = Path("utils")
        self.log_dir.mkdir(exist_ok=True)

        self.item_log = self.log_dir / item

    def _reset_log(self, log):
        now = get_current_utc_date()
        last_entry_str = log[-1].strip()
        last_entry_time = datetime.strptime(last_entry_str, "%m-%d-%Y %H:%M").replace(
            tzinfo=timezone.utc,
        )
        if now.date() > last_entry_time.date():
            with Path.open(log, "w") as file:
                file.write("")


class TrackTask:
    def __init__(self, task: str):
        log_dir = Path("utils")
        log_dir.mkdir(exist_ok=True)

        self.task_log = log_dir / (task + ".log")

        if not Path.exists(self.task_log):
            with Path.open(self.task_log, "w") as file:
                file.write("")

    def read_log(self) -> str:
        with Path.open(self.task_log) as file:
            return file.read()

    def time_since_task(self) -> int:
        """Returns time in minutes from last timestamp"""
        last_timestamp_str = self.read_log()
        try:
            last_timestamp = datetime.strptime(last_timestamp_str, "%m-%d-%Y %H:%M")
        except ValueError:
            return 999

        last_timestamp = last_timestamp.replace(tzinfo=timezone.utc)
        now = get_current_utc_date()

        return int((now - last_timestamp).total_seconds() / 60)

    def task_completed(self):
        now = get_current_utc_date()
        timestamp_str = now.strftime("%m-%d-%Y %H:%M")

        with Path.open(self.task_log, "w") as file:
            file.write(timestamp_str)
