# annotations

from __future__ import annotations
from typing import Iterable

"""
def add(a: int, b: int) -> int:
    return a + b

name: str - "This is a string type annotation"
count: int = 5
prices: Iterable[float] = [19.99, 29.99, 39.99]
"""

# optional

from typing import Optional
"""
def find_even(numbers: Iterable[int]) -> Optional[int]:
    for n in numbers:
        if n % 2 == 0:
            return n
    return None

print(find_even([1,3,5]))
print(find_even([1,2,3]))
"""

# dataclass

from dataclasses import dataclass

"""
class User:
    def __init__(self, height, weight):
        self.height = height
        self.weight = weight  

@dataclass
class User:
    height: float
    weight: float

Dung = User(1.75, 68.0)
print(Dung)
print(Dung.height)
"""  

# counter 

from collections import Counter
"""
ips=["1.1.1.1", "2.2.2.2", "1.1.1.1"]

count = Counter(ips)
print(count)
print(count.most_common(1))
"""

# defaultdict

from collections import defaultdict
"""
scores = defaultdict(int)

scores["math"] += 10
scores["math"] += 5

print(scores)
"""

# argparse

import argparse
"""
parser = argparse.ArgumentParser(description="This is a sample argparse program.")
parser.add_argument("name", help = "Your name")
parser.add_argument("-a", "--age", type=int, defaul=20, help = "Your age")

args = parser.parse_args()

print(f"Hello, {args.name}!")
if args.age:
    print(f"You are {args.age} years old.")
"""

# parsing logic

line = "GET /home 200 31, 10.0.0.1"
parts = line.split()

print(parts)

method, path, status, latency, ip = parts

print(f"Method: {method}, Path: {path}, Status: {status}, Latency: {latency}, IP: {ip}")