from __future__ import annotations
from typing import Iterable, Optional
from collections import defaultdict, Counter
import json
from models import LogRecord


def analyze(records: Iterable[LogRecord]) -> dict:
    "Phân tích các bản ghi log và trả về thống kê"
    total = 0
    error_count = 0
    failed_logins_count = 0
    successful_logins_count = 0
    banned_users_count = 0
    kicked_users_count = 0

    ip_count = Counter()

    for r in records:
        total += 1
        ip_count[r.ip] += 1

        if msg == ["CONNECTION_ERROR"]:
            error_count += 1
        if msg == ["LOGIN_FAILED"]:
            failed_logins_count += 1
        if msg == ["LOGIN_SUCCESS"]:
            successful_logins_count += 1
        if msg == ["KICK"]:
            kicked_users_count += 1
        if msg == ["BAN"]:
            banned_users_count += 1

        
        """
        latency_count[r.path] += 1
        latency_sum[r.path] += r.latency_ms
        """

    error_rate = error_count/total if total > 0 else 0

    """
    avg_latency_per_path = {
        path: (latency_sum[path]/latency_count[path])
        for path in latency_count
        if latency_count[path] > 0
    }

    avg_latency_sorted = sorted(avg_latency_per_path.items(), key=lambda x: x[1], reverse=True)
    """

    return{
        "total_requests": total,
        "successful_logins": successful_logins_count,
        "failed_logins": failed_logins_count,
        "kicked_users": kicked_users_count,
        "banned_users": banned_users_count,
        "error_count": error_count,
        "error_rate": error_rate,
        "top_5_IPs": ip_count.most_common(5)
    }