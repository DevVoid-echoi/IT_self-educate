# 🔑 Secure Password Generator (CLI)

Một ứng dụng dòng lệnh (CLI) được viết bằng Python giúp tạo mật khẩu ngẫu nhiên an toàn, hỗ trợ tùy chỉnh các thuộc tính và tự động đánh giá độ mạnh của mật khẩu.

---

## 📌 Tính năng chính

- **Tùy chỉnh linh hoạt:** Cho phép chọn độ dài mật khẩu, tích hợp/loại trừ chữ số và ký tự đặc biệt.
- **Đánh giá độ mạnh:** Tự động phân loại độ an toàn của mật khẩu theo các mức (*Yếu, Trung bình, Mạnh, Rất mạnh*).
- **Xử lý ngoại lệ:** Kiểm tra và phản hồi khi người dùng nhập dữ liệu đầu vào không hợp lệ.
- **Kiến trúc Mô-đun:** Tách biệt rõ ràng giữa logic xử lý mật khẩu (`generator.py`) và giao diện tương tác (`cli.py`).

---

## 📁 Cấu trúc dự án

```text
password_generator_final/
│
├── src/                        # Thư mục chứa mã nguồn chính
│   ├── generator.py            # Logic sinh mật khẩu & đánh giá độ mạnh
│   └── cli.py                  # Giao diện tương tác dòng lệnh (CLI)
│
├── tests/                      # Thư mục chứa các bài kiểm thử tự động
│   └── test_generator.py      # Unit tests cho logic sinh mật khẩu
│
├── main.py                     # Entry point chính để khởi chạy ứng dụng
└── README.md                   # Tài liệu hướng dẫn sử dụng