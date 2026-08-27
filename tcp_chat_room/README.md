# Multi-Threaded TCP Chat System with RBAC & Security Logging

Một hệ thống Chat Client-Server đa luồng (Multi-Threaded) viết bằng Python, tập trung vào khả năng xác thực người dùng (Authentication), phân quyền dựa trên vai trò (Role-Based Access Control - RBAC), quản trị hệ thống trực tiếp qua Server Console và ghi nhận nhật ký an ninh (Security Logging).

---

## 🌟 Tính năng nổi bật

* **Multi-Threaded Networking**: Xử lý đồng thời nhiều Client kết nối sử dụng `socket` và `threading`.
* **Authentication & Session**: Đăng ký, đăng nhập với mật khẩu mã hóa hash và quản lý phiên làm việc (`user_sessions`).
* **Role-Based Access Control (RBAC)**: Phân quyền lệnh (`/kick`, `/ban`, `/unban`) dựa trên vai trò (`admin`, `moderator`, `user`).
* **Server Console Commands**: Cho phép Server Administrator quản lý và cấp quyền (`/set <username> <role>`) trực tiếp từ Terminal máy chủ thời gian thực.
* **Real-time State Synchronization**: Đồng bộ tức thì quyền hạn mới từ cơ sở dữ liệu (`user.json`) tới Session RAM của Client đang online.
* **Security & System Logging**: Tách biệt luồng ghi log vận hành (`server.log`) và log an ninh (`security.log`) chuẩn format sản xuất.

---

## 📁 Cấu trúc dự án

```text
tcp_chat_room/
├── auth/
│   ├── authentication.py    # Xử lý login, register, hash password, set_user_role
│   ├── password.py          # Hàm mã hóa & kiểm tra mật khẩu
│   └── rbac.py              # Định nghĩa Roles & Permissions (ADMIN, MODERATOR, USER)
├── client_side/

│   ├── client_management/
│   │   ├── connection.py        # Quản lý kết nối TCP phía Client
│   │   └── instruction.py       # Hiển thị hướng dẫn lệnh động theo Role người dùng
│    └──    client.py            # Khởi chạy Client chat
│
├── data/
│   ├── ban.txt              # Danh sách tài khoản bị cấm (Banned)
│   └── user.json            # Cơ sở dữ liệu tài khoản & quyền hạn
├── logs/
│   ├── security.log         # Log đăng nhập, vi phạm quyền, lệnh KICK/BAN/UNBAN
│   └── server.log           # Log kết nối/ngắt kết nối của các client
├── server_side/
│   ├── client_management/
│   │   ├── actions.py       # Xử lý tin nhắn, câu lệnh chat, KICK, BAN, UNBAN
│   │   ├── ban_handler.py   # Xử lý ghi/đọc file cấm người dùng
│   │   └── lock.py          # Lock quản lý bất đồng bộ (state_lock)
│   ├── logs_management/
│   │   └── record_logs.py   # Module ghi nhận log an ninh & hệ thống
│   └── server.py            # Entry point khởi chạy TCP Server & Console Thread
└── config.py                # Cấu hình HOST, PORT và đường dẫn file
🛠️ Lệnh quản trị & Cú pháp
1. Phía Server Console (Nhập trực tiếp tại Terminal Server)
/set <username> <role>: Gán quyền mới cho người dùng (admin, moderator, user).

2. Phía Client Chat Room
/quit hoặc /exit: Rời khỏi phòng chat.

/kick <username>: Đẩy người dùng ra khỏi phòng chat (Yêu cầu quyền Admin/Moderator).

/ban <username>: Cấm người dùng tham gia phòng chat (Yêu cầu quyền Admin).

/unban <username>: Bỏ cấm người dùng (Yêu cầu quyền Admin).

🚀 Hướng dẫn khởi chạy
Yêu cầu môi trường
Python 3.10+ (Không cần cài đặt thư viện bên thứ ba).

1. Chạy Server
Mở Terminal tại thư mục gốc tcp_chat_room:

Bash
python3 server_side/server.py

2. Phía Client Chat Room
/quit hoặc /exit: Rời khỏi phòng chat.

/kick <username>: Đẩy người dùng ra khỏi phòng chat (Yêu cầu quyền Admin/Moderator).

/ban <username>: Cấm người dùng tham gia phòng chat (Yêu cầu quyền Admin).

/unban <username>: Bỏ cấm người dùng (Yêu cầu quyền Admin).