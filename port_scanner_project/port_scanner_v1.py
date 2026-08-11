import socket
import threading
from queue import Queue

target = input("Enter the target IP address: ") # Địa chỉ IP của máy chủ cần quét
queue = Queue() # Tạo một hàng đợi để lưu trữ các cổng cần quét
open_ports = [] # Danh sách các cổng mở
print_lock = threading.Lock() # Tạo một khóa để đồng bộ hóa việc in ra màn hình

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tạo một socket IPv4, TCP
        sock.settimeout(1.0)
        sock.connect((target, port)) # Kết nối đến địa chỉ IP và cổng được chỉ định
        sock.close()
        return True
    except (socket.error, OSError, socket.timeout): # Nếu có lỗi xảy ra khi kết nối, trả về False
        return False

def fill_queue(port_list): # Điền các cổng vào hàng đợi
    for port in port_list:
        queue.put(port)

def worker(): # Hàm worker để quét các cổng trong hàng đợi
    while True:
        try:
            port = queue.get(block=False) # Lấy một cổng từ hàng đợi, nếu hàng đợi rỗng thì dừng lại
        except:
            break

        if portscan(port):
            with print_lock: # Sử dụng khóa để đồng bộ hóa việc in ra màn hình
                print("Port {} is open".format(port)) # In ra thông báo cổng mở
                open_ports.append(port) # Thêm cổng mở vào danh sách các cổng mở

        queue.task_done()

port_list = range(1, 1024)  #Danh sách các cổng cần quét từ 1 đến 1023
fill_queue(port_list)

thread_list = []

for t in range(100): # Tạo 100 luồng để quét các cổng
    thread = threading.Thread(target=worker, daemon=True) # Tạo một luồng mới với hàm worker và đặt nó là daemon
    thread_list.append(thread)

for thread in thread_list: # Bắt đầu tất cả các luồng
    thread.start()

for thread in thread_list: # Chờ tất cả các luồng kết thúc
    thread.join()

open_ports.sort() # Sắp xếp danh sách các cổng mở theo thứ tự tăng dần
print("Open ports are: ", open_ports) # In ra danh sách các cổng mở
