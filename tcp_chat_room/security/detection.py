import os
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Iterable, List, Dict
from security.logger import log_alert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_PARSER_DIR = os.path.join(BASE_DIR, "log_parser")

from log_parser.models import LogRecord

class BruteForceDetector:
    def __init__(self, max_attempts: int=5, window_seconds: int=60):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.failed_attempts_history: Dict[str, List[datetime]] = defaultdict(list)

    def _parse_timestamp(self, date_str: str, time_str: str) -> datetime:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

    def process_record(self, record: LogRecord):
        if record.event_type != "LOGIN_FAILED" or not record.ip or record.ip == "N/A":
            return

        current_time = self._parse_timestamp(record.date, record.time)
        ip = record.ip
        timestamps = self.failed_attempts_history[ip]

        timestamps.append(current_time)

        threshold_time =current_time - timedelta(seconds=self.window_seconds)
        self.failed_attempts_history[ip] = [
            t for t in timestamps if  t>= threshold_time
        ]

        valid_attempts = len(self.failed_attempts_history[ip])
        if valid_attempts >= self.max_attempts:
            log_alert(ip=ip, failed_attempts=valid_attempts, window_seconds=self.window_seconds)
            self.failed_attempts_history[ip].clear()

def detect_brute_force_stream(records: Iterable[LogRecord], max_attempts: int=5, window_seconds: int=60):
    detector = BruteForceDetector(max_attempts=max_attempts, window_seconds=window_seconds)
    for record in records:
        detector.process_record(record)