
# 🌤️ Weather Logger

Ứng dụng ghi lại lịch sử thời tiết theo thời gian thực.

---

## Luồng hoạt động

```
Người dùng nhập thành phố
        ↓
Gọi API OpenWeatherMap → nhận JSON
        ↓
Xử lý data (nhiệt độ, độ ẩm, mô tả)
        ↓
Lưu vào PostgreSQL
```

---

## Công nghệ

| Thư viện | Vai trò |
|----------|---------|
| `requests` | Gọi API OpenWeatherMap |
| `python-dotenv` | Đọc biến môi trường từ `.env` |
| `SQLAlchemy` | Kết nối PostgreSQL |
| `psycopg2` | Driver PostgreSQL |
