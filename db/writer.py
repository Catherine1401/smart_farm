from cnosdb_connector import connect

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
