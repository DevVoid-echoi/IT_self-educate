import json
import argparse
import time
from src.port_scanner import PortScanner, parse_ports

def client_interact():
    "Tạo đối tượng argparse để xử lý tham số dòng lệnh"
    parser = argparse.ArgumentParser(description="Công cụ Port Scanner đa luồng")
    parser.add_argument("-t", "--target", required=True, help="Địa chỉ IP hoặc Domain của máy chủ cần quét")
    parser.add_argument("-p", "--ports", default="1-1024", help="Cổng cần quét (VD: 80 hoặc 1-1024 hoặc 80,443)")
    parser.add_argument("-n", "--threads", type=int, default=100, help="Số lượng luồng tối đa. Mặc định: 100")
    parser.add_argument("-s", "--timeout", type=float, default=1.0, help="Thời gian chờ kết nối tối đa cho mỗi cổng (giây). Mặc định: 1.0")
    parser.add_argument("-o", "--output", help="Đường dẫn file JSON để lưu kết quả quét")

    args = parser.parse_args()

    ports_to_scan = parse_ports(args.ports) # Chuyển chuỗi cổng thành list số 

    start_time = time.time() # Lưu thời gian bắt đầu quét
    scanner = PortScanner(
        target_host=args.target,
        ports=ports_to_scan,
        num_threads=args.threads,
        timeout=args.timeout)
    scanner.run() # Thực thi quét
    duration = time.time() - start_time # Tính thời gian quét

    # In kết quả ra màn hình dạng bảng căn chỉnh cột
    print("\n" + "=" * 50)
    print(f"KẾT QUẢ QUÉT CỔNG M MỞ ({len(scanner.open_ports)} cổng mở):")
    print("=" * 50)
    print(f"{'PORT':<10}{'SERVICE':<15}{'BANNER/INFO'}")
    print("-" * 50)

    for item in scanner.open_ports:
        print(f"{item['port']:<10}{item['service']:<15}{item['banner']}")

    print("=" * 50)
    print(f"Hoàn thành trong {duration:.2f} giây.")

    # Nếu có tham số xuất file JSON, lưu kết quả vào file
    if args.output:
        report = {
            "target": args.target,
            "ip": scanner.target_ip,
            "scan_duration": duration,
            "open_ports": scanner.open_ports
        }
        with open(args.output, 'w', encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(f"[+] Kết quả đã được lưu vào file: {args.output}")