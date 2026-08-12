from __future__ import annotations
import argparse 
from typing import Iterable, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a log file")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("-o", "--output", help="Path to the output file (optional)")

    args = parser.parse_args()

    results = analyze(iter_record(args.log_file))

    total_requests = results["total_requests"]
    error_count = results["error_count"]
    error_rate = results["error_rate"]
    top_5_IPs = results["top_5_IPs"]
    avg_latency_sorted = results["avg_latency_sorted"]

    print("\n" + "=" * 50)
    print(f"Total request: {total_requests}")
    print("-" * 50)

    print(f"Error count: {error_count}")
    print("-" * 50)

    print(f"Error rate: {error_rate:.2%}")
    print("-" * 50)

    print("Top 5 IPs:")
    for ip, count in top_5_IPs:
        print(f"{ip}:{count}")
    print("-" * 50)

    print ("Average latency per path (sorted):")
    for path, avg_latency in avg_latency_sorted:
        print(f"{path}: {avg_latency:.2f} ms")

    print("=" * 50)

    if args.output:
        report = {
            "total_requests": total_requests,
            "error_count": error_count,
            "error_rate": error_rate,
            "top_5_IPs": top_5_IPs,
            "avg_latency_sorted": avg_latency_sorted
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
            print(f"[+] Kết quả đã được lưu vào file: {args.output}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())


   