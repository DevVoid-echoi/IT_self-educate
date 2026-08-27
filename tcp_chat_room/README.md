Dưới đây là toàn bộ mã nguồn Markdown hoàn chỉnh cho file **`README.md`**. Bạn chỉ cần sao chép toàn bộ nội dung trong khung bên dưới và dán trực tiếp vào file `README.md` ở thư mục gốc của dự án.

```markdown
# Multi-Threaded TCP Chat System with RBAC & Security Logging

Một hệ thống Chat Client-Server đa luồng (Multi-Threaded) xây dựng trên nền tảng Python Pure-Socket. Dự án tập trung vào kiến trúc bảo mật với cơ chế xác thực người dùng (Authentication), phân quyền truy cập theo vai trò (Role-Based Access Control - RBAC), quản trị hệ thống trực tiếp qua Server Console và ghi nhận nhật ký an ninh (Security Logging) theo chuẩn production.

---

## 🌟 Tính năng nổi bật

* **Multi-Threaded Architecture**: Xử lý đồng thời nhiều Client kết nối sử dụng `socket` và `threading` với cơ chế khóa bất đồng bộ (`state_lock`) an toàn.
* **Authentication & Session Management**: Đăng ký, đăng nhập với mật khẩu được mã hóa Hash (Bcrypt/SHA-256) và quản lý phiên làm việc (`user_sessions`).
* **Role-Based Access Control (RBAC)**: Phân quyền thực thi câu lệnh (`/kick`, `/ban`, `/unban`) linh hoạt theo danh mục vai trò (`admin`, `moderator`, `user`).
* **Server Console Control**: Cho phép Administrator cấp quyền linh hoạt (`/set <username> <role>`) trực tiếp từ Terminal Server theo thời gian thực.
* **Real-time Session Synchronization**: Tự động đồng bộ quyền hạn mới từ file lưu trữ (`user.json`) tới RAM Session của Client đang online mà không cần tái kết nối.
* **Security & System Logging**: Tách biệt luồng ghi log vận hành (`server.log`) và log an ninh (`security.log`) tự động ép ghi xuống đĩa (`flush`). Không lưu trữ password dưới dạng plain-text.

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
    │    ├──    connection.py        # Quản lý kết nối TCP phía Client
│   │   └── instruction.py       # Hiển thị hướng dẫn lệnh động theo Role người dùng
│   └──    client.py            # Khởi chạy Client chat
│
├── data/
│   ├── ban.txt              # Cơ sở dữ liệu danh sách tài khoản bị cấm (Banned)
│   └── user.json            # Cơ sở dữ liệu tài khoản & quyền hạn RBAC
├── logs/
│   ├── security.log         # Log đăng nhập, vi phạm quyền, lệnh KICK/BAN/UNBAN
│   └── server.log           # Log kết nối, ngắt kết nối và luồng vận hành hệ thống
├── server_side/
│   ├── client_management/
│   │   ├── actions.py       # Điều hướng tin nhắn, xử lý lệnh KICK, BAN, UNBAN
│   │   ├── ban_handler.py   # Module đọc/ghi danh sách người dùng bị cấm
│   │   └── lock.py          # Lock quản lý bất đồng bộ tránh race condition (state_lock)
│   ├── logs_management/
│   │   └── record_logs.py   # Module khởi tạo và ghi log chuẩn logging
│   └── server.py            # Entry point khởi chạy TCP Server & Console Thread
├── config.py                # Cấu hình tham số PORT, HOST và đường dẫn dữ liệu
└── README.md                # Tài liệu hướng dẫn dự án

```

---

## 🛠️ Danh mục lệnh & Cú pháp

### 1. Phía Server Console (Nhập tại Terminal máy chủ)

* `/set <username> <role>`: Gán role mới cho người dùng (`admin`, `moderator`, `user`).

### 2. Phía Client Chat Room

* `/quit` hoặc `/exit`: Rời khỏi phòng chat.
* `/kick <username>`: Đẩy người dùng ra khỏi phòng chat *(Yêu cầu quyền KICK)*.
* `/ban <username>`: Cấm người dùng tham gia phòng chat vĩnh viễn *(Yêu cầu quyền BAN)*.
* `/unban <username>`: Bỏ cấm người dùng khỏi hệ thống *(Yêu cầu quyền UNBAN)*.

---

## 🚀 Hướng dẫn khởi chạy

### Yêu cầu môi trường

* **Python 3.10+** (Chạy trên các thư viện chuẩn của Python, không cần cài đặt package bên ngoài).

### Bước 1: Khởi chạy Server

Mở Terminal tại thư mục gốc `tcp_chat_room`:

```bash
python3 server_side/server.py

```

### Bước 2: Khởi chạy Client

Mở một cửa sổ Terminal khác và thực hiện:

```bash
python3 client_side/client.py

```

---

## 📝 Định dạng Security Log (`logs/security.log`)

Toàn bộ các sự kiện liên quan đến an ninh và xác thực đều được tự động lưu trữ dưới định dạng chuẩn:

```text
2026-08-27 15:00:10 INFO USER_CONNECTED username=N/A ip=127.0.0.1
2026-08-27 15:00:15 INFO LOGIN_SUCCESS username=alice ip=127.0.0.1
2026-08-27 15:00:22 WARNING LOGIN_FAILED username=bob ip=127.0.0.1
2026-08-27 15:01:05 WARNING KICK username=spammer by=admin
2026-08-27 15:01:10 WARNING BAN username=spammer by=admin

```

```

```