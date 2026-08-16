import socket
import threading
import argparse
import json
import time
from queue import Queue
from tqdm import tqdm

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 5000: "AirPlay/Flask", 5500: "LiveServer", 5432: "PostgreSQL", 
    6463: "Discord-RPC", 8080: "HTTP-Proxy", 9993: "ZeroTier"
}

class PortScanner:
    def __init__(self, target_host, ports, num_threads=100, timeout=1.0):
        self.target_host = target_host
        self.target_ip = self._resolve_target(target_host)
        self.ports = ports
        self.num_threads = num_threads
        self.timeout = timeout
        self.queue = Queue()
        self.open_ports = []
        self.print_lock = threading.Lock()
        self.progress_bar = None

    def _resolve_target(self, host):
        "Chuyển đổi Domain thành IP và kiểm tra tính hợp lệ"
        try:
            return socket.gethostbyname(host) # Gọi DNS để lấy IP từ hostname
        except socket.gaierror: # Bắt lỗi nếu sai IP hoặc tên miền không tồn tại
            print(f"[!] Lỗi: Không thể phân giải địa chỉ '{host}'. Hãy kiểm tra lại IP/Domain.")
            exit(1) # Dừng chương trình
    
    def _grab_banner(self, sock):
        "Đọc banner từ dịch vụ để xác định loại service"
        try:
            # Gửi truy vấn HTTP cơ bản để kích thích server phản hồi
            sock.send(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")
            # Nhận tối đa 1024 bytes dữ liệu trả về và giải mã utf-8
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            # Lấy dòng đầu tiên của banner phản hồi
            return banner.split('\n')[0] if banner else "Unknown Service"
        except:
            return "Unknown Service"

    def _analyze_service(self,port, banner):
        "Tự động suy luận dịch vụ dựa trên Port và nội dung Banner."
        if port in COMMON_SERVICES:
            return COMMON_SERVICES[port]

        banner_lower = banner.lower()

        if "http" in banner_lower or "html" in banner_lower:
            return "HTTP Web Service"
        elif "jsonrpc" in banner_lower or "desktop_api" in banner_lower:
            return "RPC/API Service"
        elif "ssh" in banner_lower:
            return "SSH"
        elif "ftp" in banner_lower:
            return "FTP"
        elif "smtp" in banner_lower:
            return "SMTP"
        elif "mysql" in banner_lower:
            return "MySQL"
        elif "tier1" in banner_lower or "spotify" in banner_lower:
            return "Local App Service"

        return "Unknown"

    def _scan_port(self, port):
        "Thực hiện kết nối thử nghiệm đến cổng"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tạo socket IPv4, TCP
            sock.settimeout(self.timeout) # Thời gian chờ tối đa
            result = sock.connect_ex((self.target_ip, port)) # Thử kết nối (Return 0 nếu thành công)

            if result == 0:
                banner = self._grab_banner(sock) # Thử đọc banner
                service_name = self._analyze_service(port,banner)
                sock.close()
                return True, service_name, banner
            
            sock.close()
            return False, None, None
        except (socket.error, OSError):
                return False, None, None

    def _worker(self):
        "Hàm xử lý luồng lấy nhiệm vụ từ Queue"
        while True:
            try:
                port = self.queue.get_nowait() # Lấy 1 cổng từ hàng đợi (không đợi nếu rỗng)
            except:
                break

            is_open, service, banner = self._scan_port(port) # Quét cổng
            if is_open:
                port_data = {
                    "port": port,
                    "service": service,
                    "banner": banner
                }
                with self.print_lock: # Khoá luồng trước khi ghi vào mảng chung
                    self.open_ports.append(port_data)
            
            with self.print_lock: # Khoá luồng trước khi cập nhật thanh tiến trình 
                if self.progress_bar:
                    self.progress_bar.update(1) # Tăng thanh tiến trình lên 1 đơn vị

            self.queue.task_done() # Báo cho queue biết hoàn thành

    def run(self):
        "Khởi chạy quá trình quét"
        print(f"[*] Bắt đầu quét mục tiêu: {self.target_host} ({self.target_ip})")
        print(f"[*] Số lượng cổng quét: {len(self.ports)} | Số luồng: {self.num_threads}\n")

        # Nạp toàn bộ cổng vào hàng đợi queue
        for port in self.ports:
            self.queue.put(port)

        # Khởi tạo đối tượng thanh tiến trình tqdm
        self.progress_bar = tqdm(total=len(self.ports), desc="Tiến trình", unit="port")

        threads = []
        # Tạo số lượng luồng
        for _ in range(min(self.num_threads, len(self.ports))):
            thread = threading.Thread(target=self._worker, daemon=True)
            threads.append(thread)
            thread.start() # Bắt đầu luồng

        for thread in threads:
            thread.join() # Chờ tất cả các luồng hoàn thành công việc

        self.progress_bar.close() # Đóng thanh tiến trình
        self.open_ports.sort(key=lambda x: x["port"]) 

def parse_ports(port_str):
    "Phân tích chuỗi đầu vào của cổng"
    ports = set()
    try:
        parts = port_str.split(',')
        for part in parts:
            if '-' in part: # Nếu là dải cổng
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else: # Nếu là cổng đơn
                ports.add(int(part))
            #Lọc các cổng hợp lệ (1-65535)
        return sorted([p for p in ports if 1<=p<=65535])
    except ValueError:
        print("[!] Lỗi: Chuỗi cổng không hợp lệ. Vui lòng nhập đúng định dạng: 80 hoặc 1-1024 hoặc 80,443.")
        exit(1)


