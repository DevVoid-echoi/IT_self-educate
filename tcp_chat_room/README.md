# 💬 Python TCP Multi-room Chat Application

Ứng dụng phòng chat thời gian thực (Real-time Chat) dựa trên giao thức TCP Socket và Đa luồng (Multithreading) bằng Python. Dự án hỗ trợ phân quyền Admin, các lệnh quản trị viên (`/kick`, `/ban`), cấm người dùng truy cập và cấu trúc mô-đun hóa dễ mở rộng.

---

## 🛠️ Cấu trúc dự án

```text
tcp_chat_room/
├── config.py                     # Cấu hình chung (HOST, PORT, ...)
├── data
    └── ban.txt                        # Danh
sách người dùng bị cấm
│
├── server_side/                        # Mã nguồn phía Server
│   ├── server.py                  # File khởi chạy Server chính
│   └── client_management/         # Quản lý Client & Luồng phía Server
│       ├── lock.py                # Quản lý Threading Lock
│       ├── ban_handler.py           # Xử lý danh sách cấm (Ban List)
│       └── actions.py      # Xử lý kết nối, Broadcast, Kick/Ban
│
└── client_side/                   # Mã nguồn phía Client
    ├── client.py              # File khởi chạy Client chính
    └── client_management/         # Mô-đun hỗ trợ Client
        ├── instructions.py        # Hiển thị hướng dẫn
        └── connection.py          # Luồng gửi/nhận tin nhắn Socket