import random
from pathlib import Path

PATHS = ["/", "/login", "/products", "/orders", "/metrics", "/health", "/checkout", "/user/profile"]
STATUS_CODES = [200, 200, 200, 200, 200, 201, 301, 400, 401, 404, 500, 502]
METHODS = ["GET", "POST", "PUT", "DELETE"]

def generate_ip() -> str:
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def get_next_log_filename(base_dir: Path) -> Path:
    """Tự động tìm số thứ tự lớn nhất và trả về tên file tiếp theo (access_1.log, access_2.log, ...)."""
    counter = 1
    while True:
        file_path = base_dir / f"access_{counter}.log"
        if not file_path.exists():
            return file_path
        counter += 1

def generate_log_file(total_lines: int = 1000):
    # Lấy thư mục gốc (nơi đặt script)
    base_dir = Path(__file__).resolve().parent
    output_path = get_next_log_filename(base_dir)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated Log File\n")
        f.write("# Format: <method> <path> <status> <latency_s> <ip>\n\n")

        for _ in range(total_lines):
            method = random.choice(METHODS)
            path = random.choice(PATHS)
            status = random.choice(STATUS_CODES)
            latency = round(random.uniform(500.0, 3000.0) if status >= 500 else random.uniform(1.0, 250.0), 2)
            ip = generate_ip()

            f.write(f"{method} {path} {status} {latency} {ip}\n")

    print(f" Đã khởi tạo thành công file: {output_path.name}")

if __name__ == "__main__":
    generate_log_file(1000)