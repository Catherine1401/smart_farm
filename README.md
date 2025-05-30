## Cấu trúc thư mục của dự án
---
smart_farm_project/
├── README.md
├── requirements.txt
├── .env                       # Thông tin kết nối CNOSDB
├── .gitignore

├── config/
│   └── cnosdb_config.py       # Thông tin cấu hình CNOSDB

├── data/
│   └── sample_data.json       # Dữ liệu mô phỏng mẫu (nếu cần dump thủ công)

├── sensors/                   # Sinh dữ liệu cảm biến giả
│   ├── __init__.py
│   ├── generator.py           # Hàm tạo dữ liệu giả (nhiệt độ, độ ẩm...)
│   └── scheduler.py           # Lập lịch gửi dữ liệu liên tục

├── db/
│   ├── __init__.py
│   ├── writer.py              # Ghi dữ liệu vào CnosDB
│   └── query.py               # Truy vấn dữ liệu từ CnosDB

├── logic/
│   ├── __init__.py
│   └── decision_engine.py     # Logic ra quyết định thông minh (tưới cây, bật đèn...)

├── ui/
│   ├── __init__.py
│   └── dashboard.py           # Giao diện đơn giản (có thể dùng Streamlit / Tkinter)

├── utils/
│   └── helpers.py             # Hàm tiện ích chung: logging, thời gian, format...

├── distributed/
│   └── cnosdb_cluster.md      # Tài liệu thiết lập cluster, phân tán, load balance

├── tests/
│   ├── test_generator.py
│   ├── test_writer.py
│   └── test_logic.py

└── main.py                    # Entry point: chạy mô phỏng toàn bộ hệ thống

#### Giải thích ngắn gọn

| Thư mục / File | Vai trò                                                         |
| -------------- | --------------------------------------------------------------- |
| `sensors/`     | Tạo dữ liệu giả như cảm biến đo nhiệt độ, độ ẩm...              |
| `db/`          | Giao tiếp với CnosDB: ghi + truy vấn dữ liệu                    |
| `logic/`       | Xử lý logic thông minh: đưa ra hành động khi dữ liệu đạt ngưỡng |
| `ui/`          | Dashboard hoặc giao diện đơn giản hiển thị kết quả              |
| `utils/`       | Các hàm phụ như log, thời gian, định dạng...                    |
| `config/`      | File cấu hình, ví dụ: host, port của CnosDB                     |
| `distributed/` | Hướng dẫn & cấu hình hệ thống phân tán                          |
| `tests/`       | Unit test cho từng module                                       |
| `main.py`      | Tập hợp tất cả các phần lại để chạy toàn hệ thống               |
