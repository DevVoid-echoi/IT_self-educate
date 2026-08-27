from __future__ import annotations
from typing import Iterable, Optional
import json
from models import LogRecord

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
    if len(parts) != 7:
        return None
    date, time, event_type, msg, username, ip, extra_info = parts
    
    return LogRecord(date=date, time=time, event_type=event_type, msg=msg, username=username, ip=ip, extra_info=extra_info)