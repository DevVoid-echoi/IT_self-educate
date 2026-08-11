# Multithreaded Python Port Scanner

Một công cụ quét cổng TCP đa luồng nhẹ, tốc độ cao được viết bằng Python.

## Tính năng
- **Đa luồng (Multithreading):** Tăng tốc độ quét cổng thông qua cơ chế Queue và Threading.
- **Linh hoạt chọn cổng:** Hỗ trợ quét cổng lẻ, dải cổng (`1-1000`) hoặc kết hợp (`22,80,443`).
- **Phân giải tên miền:** Chấp nhận cả IP address và Hostname/Domain.
- **Banner Grabbing:** Đọc thông tin header/service cơ bản trả về từ cổng mở.
- **Thanh tiến trình:** Tích hợp `tqdm` hiển thị phần trăm hoàn thành theo thời gian thực.
- **Xuất báo cáo:** Hỗ trợ lưu kết quả dưới dạng JSON.

## Cài đặt
```bash
pip install -r requirements.txt