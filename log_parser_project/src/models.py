from __future__ import annotations
import argparse 
from typing import Iterable, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class LogRecord: 
    "Định nghĩa cấu trúc dữ liệu cho một bản ghi log"
    path: str
    status: int
    latency_ms: float
    ip: str