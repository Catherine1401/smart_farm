import streamlit as st
st.set_page_config(page_title="🌿 Smart Farm Dashboard", layout="wide")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.query import get_station_list, query_multiple_stations

import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# 🔁 Auto-refresh mỗi 1 giây
st_autorefresh(interval=1000, key="refresh")

# 🎯 HEADER
st.title("🌿 Smart Farm Realtime Dashboard")
st.markdown("Xem dữ liệu cảm biến theo thời gian thực từ 1000 vùng canh tác.")

# 🛰️ Lấy danh sách vùng
stations = get_station_list()
if not stations:
    st.error("❌ Không lấy được danh sách vùng. Vui lòng kiểm tra kết nối hoặc dữ liệu.")
    st.stop()

# 🎛️ Sidebar: tùy chọn
with st.sidebar:
    st.header("⚙️ Tùy chọn hiển thị")
    selected_stations = st.multiselect("📍 Vùng theo dõi", stations, default=stations[:2])
    minutes_range = st.slider("⏳ Dữ liệu trong bao nhiêu phút gần đây", 1, 60, 5)
    limit_per_station = st.slider("📦 Số bản ghi mỗi vùng", 100, 2000, 1000, step=100)

if not selected_stations:
    st.warning("⚠️ Vui lòng chọn ít nhất một vùng.")
    st.stop()

# 📥 Truy vấn dữ liệu từng vùng bằng đa luồng (tối đa 32 luồng)
df = query_multiple_stations(
    selected_stations,
    limit=limit_per_station,
    max_workers=32
)

if df.empty:
    st.warning("⚠️ Không có dữ liệu từ các vùng được chọn.")
    st.stop()

# 🕒 Chuyển định dạng thời gian
df['time'] = pd.to_datetime(df['time'], utc=True)

# 🕒 Lọc dữ liệu theo thời gian gần đây
now_utc = pd.Timestamp.utcnow()
min_time = now_utc - pd.Timedelta(minutes=minutes_range)
df_filtered = df[df['time'] >= min_time]

if df_filtered.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc theo thời gian.")
    st.stop()

# 🧊 Lấy dữ liệu mới nhất của từng vùng
latest_data = df_filtered.sort_values("time", ascending=False).drop_duplicates("station")

# 📋 Bảng dữ liệu mới nhất
st.subheader("📊 Dữ liệu mới nhất theo vùng đã chọn")
st.dataframe(latest_data, use_container_width=True)

# 🚨 Cảnh báo theo ngưỡng
warnings = []
for _, row in latest_data.iterrows():
    if row.get('temperature', 0) > 35:
        warnings.append(f"🔥 Nhiệt độ cao bất thường ở {row['station']}")
    if row.get('humidity', 100) < 30:
        warnings.append(f"💨 Độ ẩm thấp ở {row['station']}")
    if row.get('soil_moisture', 100) < 15:
        warnings.append(f"🌱 Độ ẩm đất thấp ở {row['station']}")

if warnings:
    st.error("🚨 Cảnh báo môi trường:")
    for w in warnings:
        st.markdown(f"- {w}")

# 📈 Biểu đồ dữ liệu cảm biến
tabs = st.tabs(["🌡️ Nhiệt độ", "💧 Độ ẩm", "🌱 Độ ẩm đất"])

with tabs[0]:
    st.subheader("📈 Nhiệt độ (°C)")
    fig = px.line(df_filtered, x="time", y="temperature", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("📈 Độ ẩm không khí (%)")
    fig = px.line(df_filtered, x="time", y="humidity", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("📈 Độ ẩm đất (%)")
    fig = px.line(df_filtered, x="time", y="soil_moisture", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# 📋 Bảng tổng hợp cuối
st.markdown("---")
st.subheader("📋 Dữ liệu tổng hợp mới nhất")
st.dataframe(
    latest_data[['station', 'temperature', 'humidity', 'soil_moisture', 'time']],
    use_container_width=True
)

# 📊 Thống kê nhanh
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌡️ Trung bình nhiệt độ", f"{latest_data['temperature'].mean():.2f} °C")
with col2:
    st.metric("💧 Trung bình độ ẩm", f"{latest_data['humidity'].mean():.2f} %")
with col3:
    st.metric("🌱 Trung bình độ ẩm đất", f"{latest_data['soil_moisture'].mean():.2f} %")

st.caption(f"⏱️ Cập nhật lúc: {pd.Timestamp.now(tz='Asia/Ho_Chi_Minh').strftime('%H:%M:%S')}")
