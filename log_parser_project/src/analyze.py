from __future__ import annotations
import argparse 
from typing import Iterable, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import json


def analyze(records: Iterable[LogRecord]) -> dict:
    "Phân tích các bản ghi log và trả về thống kê"
    total = 0
    error_count = 0

    ip_count = Counter()
    latency_count = defaultdict(int)
    latency_sum = defaultdict(float)

    for r in records:
        total += 1
        ip_count[r.ip] += 1

        if r.status >= 400:
            error_count += 1
        
        latency_count[r.path] += 1
        latency_sum[r.path] += r.latency_ms

    error_rate = error_count/total if total > 0 else 0

    avg_latency_per_path = {
        path: (latency_sum[path]/latency_count[path])
        for path in latency_count
        if latency_count[path] > 0
    }

    avg_latency_sorted = sorted(avg_latency_per_path.items(), key=lambda x: x[1], reverse=True)

    return{
        "total_requests": total,
        "error_count": error_count,
        "error_rate": error_rate,
        "top_5_IPs": ip_count.most_common(5),
        "avg_latency_sorted": avg_latency_sorted
    }