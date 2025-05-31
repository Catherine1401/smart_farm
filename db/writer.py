from cnosdb_connector import connect
from typing import List, Tuple

# Khởi tạo kết nối (chỉnh URL, user, password cho đúng)
conn = connect(url="http://127.0.0.1:8902/", user="root", password="")

def write_to_cnosdb(measurement: str, tags: str, fields: str):
    """
    Viết dữ liệu vào CnosDB theo Line Protocol:
    measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp(optional)

    Tham số:
    - measurement: tên measurement (ví dụ "smart_farm")
    - tags: chuỗi tag, ví dụ "station=Field-1"
    - fields: chuỗi field, ví dụ "temperature=25.3,humidity=70"

    Hàm sẽ tạo dòng line protocol rồi gọi write_lines để ghi.
    """
    line = f"{measurement},{tags} {fields}"
    conn.write_lines([line])

def batch_write_to_cnosdb(data_points: List[Tuple[str, str, str]], batch_size: int = 100):
    """
    Write multiple data points to CnosDB in batches for better performance.
    
    Parameters:
    - data_points: List of tuples (measurement, tags, fields)
    - batch_size: Number of points to write in each batch
    """
    for i in range(0, len(data_points), batch_size):
        batch = data_points[i:i + batch_size]
        lines = [f"{m},{t} {f}" for m, t, f in batch]
        conn.write_lines(lines)
