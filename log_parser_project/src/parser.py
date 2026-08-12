from __future__ import annotations
import argparse 
from typing import Iterable, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

def iter_record(log_file: str) -> Iterable[LogRecord]:
    "Đọc từng dòng trong file log và trả về các bản ghi log hợp lệ"
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = parse_line(line)
            if rec is not None:
                yield rec

def parse_line(line: str) -> Optional[LogRecord]:
    "Phân tích một dòng log và trả về bản ghi log nếu hợp lệ"
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = line.split()
    if len(parts) != 5:
        return None
    _method, path, status_s, latency_s, ip = parts

    try:
        status = int(status_s)
        latency_ms = float(latency_s)
    except ValueError:
        return None
    
    return LogRecord(path=path, status=status, latency_ms=latency_ms, ip=ip)