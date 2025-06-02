# Hệ Thống Giám Sát & Điều Khiển Nông Trại Thông Minh sử dụng CnosDB

### Môn học: Ứng dụng phân tán — Đại học Phenikaa  
**Giảng viên hướng dẫn:** Phạm Kim Thành  
**Lớp:** Ứng dụng phân tán*-1-3-24(N05)  
**Nhóm 07:**  
- Nguyễn Thị Dung — 22010471  
- Vũ Viết Huy — 23010699

---

## Giới thiệu Dự án

Dự án xây dựng một **hệ thống giám sát và điều khiển nông trại thông minh** sử dụng **CnosDB**, một cơ sở dữ liệu mã nguồn mở tối ưu cho dữ liệu chuỗi thời gian. Hệ thống mô phỏng và theo dõi các thông số môi trường trong thời gian thực với kiến trúc phân tán, hỗ trợ bảng điều khiển trực quan, sinh dữ liệu đa luồng và phản ứng tự động.

---

## Tại sao là Nông trại thông minh?

Nông nghiệp hiện đại ngày càng áp dụng công nghệ như IoT và AI, đòi hỏi hệ thống theo dõi dữ liệu hiệu quả, thời gian thực. Dự án này giải quyết các vấn đề:

- Thiếu giám sát môi trường thời gian thực
- Hoạt động canh tác thủ công, dễ sai sót
- Khó lưu trữ và xử lý dữ liệu chuỗi thời gian
- Hệ thống không mở rộng và khó bảo trì

**Mục tiêu:** Xây dựng một hệ thống giám sát nhẹ, dễ mở rộng, thời gian thực dựa trên công nghệ phân tán hiện đại và cơ sở dữ liệu CnosDB.

---

## Kiến trúc Hệ thống

Gồm các thành phần chính:

1. **Sensor Node**: Mô phỏng cảm biến môi trường (nhiệt độ, độ ẩm, ánh sáng…)
2. **Gateway**: Tổng hợp và gửi dữ liệu đến Load Balancer
3. **Load Balancer**: Điều phối dữ liệu đến các node CnosDB
4. **CnosDB Cluster**: Lưu trữ và truy vấn dữ liệu thời gian thực
5. **Xử lý Đa luồng**:
    - Ghi dữ liệu
    - Đọc dữ liệu
    - Phân tích bất thường
    - Ra quyết định điều khiển
6. **Giao diện người dùng**: Dashboard Streamlit trực quan theo thời gian thực

---

## Cấu trúc Dự án

```bash
smart_farm/
├── config/                # Cấu hình CnosDB
├── db/                    # Logic đọc/ghi dữ liệu
├── sensors/               # Mô phỏng cảm biến
├── ui/                    # Giao diện dashboard Streamlit
├── distributed/           # Cluster CnosDB phân tán
├── images/                # Sơ đồ, ảnh minh họa
├── main.py                # File chạy chính
├── requirements.txt       # Thư viện cần thiết
└── README.md              # File hướng dẫn
```
## Công nghệ sử dụng
---
#### Ngôn ngữ

- Python — Cú pháp rõ ràng, dễ viết, thư viện phong phú

#### Thư viện chính

| Thư viện                | Mục đích                    |
| ----------------------- | --------------------------- |
| `streamlit`             | Giao diện người dùng        |
| `streamlit_autorefresh` | Tự động làm mới UI          |
| `plotly.express`        | Vẽ biểu đồ tương tác        |
| `pandas`                | Phân tích dữ liệu           |
| `concurrent.futures`    | Xử lý đa luồng              |
| `urllib.request`        | Kết nối API                 |
| `datetime`              | Xử lý thời gian             |
| `random`                | Mô phỏng dữ liệu ngẫu nhiên |

#### Cơ sở dữ liệu

- **CnosDB**: Cơ sở dữ liệu chuỗi thời gian mã nguồn mở, tối ưu cho dữ liệu IoT, hỗ trợ phân tán và truy vấn hiệu quả.

## Bắt đầu
---
#### Yêu cầu

- Python 3.x
- Docker
- Git
- Linux (Debian/Ubuntu được khuyến nghị)

#### Cài đặt
```bash
# Bước 1: Clone dự án
git clone https://github.com/Catherine1401/smart_farm.git
cd smart_farm

# Bước 2: Chạy hệ thống
python3 main.py
```
## Quy trình hoạt động
---
1. Cảm biến tạo dữ liệu liên tục
2. Gateway gửi dữ liệu đến Load Balancer
3. Load Balancer điều hướng đến các node CnosDB
4. CnosDB lưu trữ và phục vụ truy vấn
5. Dashboard hiển thị dữ liệu trực tiếp
6. Bộ điều khiển đưa ra cảnh báo/hành động khi phát hiện bất thường

## Tính năng hiện tại
---
- Dashboard thời gian thực
- Mô phỏng 1000+ trạm cảm biến
- Đa luồng xử lý dữ liệu
- Cảnh báo khi dữ liệu vượt ngưỡng
- Bảng điều khiển điều khiển tưới tiêu

## Hướng phát triển
---
#### Phiên bản cộng đồng (poor version)

- Chạy nhiều instance CnosDB thủ công
- Sử dụng reverse proxy hoặc phân mảnh dữ liệu theo mã hóa
- hiết lập điều phối đơn giản (stateless routing)

#### Phiên bản doanh nghiệp (rich version)

- Cluster CnosDB bản enterprise:
    - Tự động chia nhỏ dữ liệu
    - Cân bằng tải & sẵn sàng cao
    - Node riêng cho metadata và storage

## Kết luận
---
Dự án xây dựng thành công mô hình nguyên mẫu hệ thống giám sát nông trại thông minh sử dụng CnosDB. Hệ thống hoạt động ổn định, có khả năng mở rộng và xử lý dữ liệu thời gian thực hiệu quả. Đây là bước đầu quan trọng trong việc áp dụng công nghệ phân tán vào nông nghiệp thông minh.

**Link source code:** [GitHub Repository](https://github.com/Catherine1401/smart_farm.git)

*Hà Nội, tháng 6 năm 2025*

*Đại học Phenikaa — Nhóm 07*