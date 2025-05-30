import streamlit as st
st.set_page_config(page_title="🌿 Smart Farm Dashboard", layout="wide")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.query import query_latest_data

import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# 🔁 Auto-refresh mỗi 1s
st_autorefresh(interval=1000, key="refresh")

# 🎯 HEADER
st.title("🌿 Smart Farm Realtime Dashboard")
st.markdown("Xem dữ liệu cảm biến theo thời gian thực từ 10 vùng canh tác.")

# 📥 Lấy dữ liệu
df = query_latest_data(limit=1000)  # lấy nhiều để biểu đồ đẹp hơn

if df.empty:
    st.warning("⚠️ Không có dữ liệu.")
    st.stop()

# Chuẩn hóa
df['time'] = pd.to_datetime(df['time'])
stations = sorted(df['station'].unique().tolist())

# 🎚️ SIDEBAR
with st.sidebar:
    st.header("⚙️ Tùy chọn hiển thị")
    selected_stations = st.multiselect("📍 Vùng theo dõi", stations, default=stations)
    minutes_range = st.slider("⏳ Dữ liệu trong bao nhiêu phút gần đây", 1, 60, 5)

# 📊 Lọc dữ liệu
df = df[df['station'].isin(selected_stations)]
min_time = pd.Timestamp.now() - pd.Timedelta(minutes=minutes_range)
df = df[df['time'] >= df['time'].min()] if df['time'].min() > min_time else df[df['time'] >= min_time]


# 📌 Dữ liệu mới nhất mỗi vùng
latest_data = df.sort_values("time", ascending=False).drop_duplicates("station")

# 🔔 Cảnh báo nếu vượt ngưỡng
warning_cols = []
for _, row in latest_data.iterrows():
    if row['temperature'] > 35:
        warning_cols.append(f"🔥 Nhiệt độ cao bất thường ở {row['station']}")
    if row['humidity'] < 30:
        warning_cols.append(f"💨 Độ ẩm thấp ở {row['station']}")
    if row['soil_moisture'] < 15:
        warning_cols.append(f"🌱 Độ ẩm đất thấp ở {row['station']}")

if warning_cols:
    st.error("🚨 Cảnh báo môi trường:")
    for w in warning_cols:
        st.markdown(f"- {w}")

# 📈 BIỂU ĐỒ
tabs = st.tabs(["🌡️ Nhiệt độ", "💧 Độ ẩm", "🌱 Độ ẩm đất"])

with tabs[0]:
    st.subheader("📈 Nhiệt độ (°C)")
    fig = px.line(df, x="time", y="temperature", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("📈 Độ ẩm không khí (%)")
    fig = px.line(df, x="time", y="humidity", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("📈 Độ ẩm đất (%)")
    fig = px.line(df, x="time", y="soil_moisture", color="station", markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# 🧊 TỔNG QUAN DỮ LIỆU MỚI NHẤT
st.markdown("---")
st.subheader("📋 Dữ liệu mới nhất mỗi vùng")
st.dataframe(latest_data[['station', 'temperature', 'humidity', 'soil_moisture', 'time']], use_container_width=True)

# 📊 Biểu đồ cột tóm tắt
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡️ Trung bình nhiệt độ", f"{latest_data['temperature'].mean():.2f} °C")

with col2:
    st.metric("💧 Trung bình độ ẩm", f"{latest_data['humidity'].mean():.2f} %")

with col3:
    st.metric("🌱 Trung bình độ ẩm đất", f"{latest_data['soil_moisture'].mean():.2f} %")

st.caption(f"⏱️ Cập nhật lúc: {pd.Timestamp.now().strftime('%H:%M:%S')}")
