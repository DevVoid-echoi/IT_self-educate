# Log Parser Project

Chương trình xử lý và phân tích file log bằng Python. Dự án đọc các bản ghi log hệ thống/web server, phân tích cú pháp (parse) dữ liệu, và tính toán thời gian phản hồi trung bình (average latency) theo từng đường dẫn (path).

## Tính năng

- **Log Parsing**: Đọc từng dòng từ file log, hỗ trợ bỏ qua các dòng trống hoặc dòng chú thích (`#`).
- **Data Validation**: Kiểm tra tính hợp lệ của cấu trúc dòng log và tự động xử lý ngoại lệ dữ liệu.
- **Latency Analysis**: Thống kê và sắp xếp thời gian phản hồi trung bình (`latency_ms`) theo từng `path`.

## Cấu trúc File Log Input

File log (ví dụ: `access.log`) cần tuân theo định dạng các trường phân cách bằng khoảng trắng:
```text
<method> <path> <status> <latency_s> <ip>