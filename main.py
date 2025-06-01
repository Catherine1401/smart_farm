import subprocess
import threading
import time
import os
import sys
import socket

# === CONFIG ===
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
CNOSDB_PORT = 8902

# === TẠO VENV & INSTALL DEPENDENCIES ===
def setup_virtualenv():
    """Tạo môi trường ảo nếu chưa có và cài đặt dependencies."""
    if not os.path.isdir(VENV_DIR):
        print("[ENV] Tạo môi trường ảo...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR])

    pip_executable = os.path.join(VENV_DIR, "bin", "pip")
    python_executable = os.path.join(VENV_DIR, "bin", "python")

    print("[ENV] Cài đặt dependencies từ requirements.txt...")
    subprocess.run([pip_executable, "install", "--upgrade", "pip"])
    subprocess.run([pip_executable, "install", "-r", REQUIREMENTS_FILE])

    return python_executable

# === CNOSDB ===
def is_cnosdb_running(host="localhost", port=CNOSDB_PORT):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False

def start_cnosdb_docker():
    """Khởi động CnosDB container nếu chưa chạy."""
    print("[DOCKER] Kiểm tra container 'cnosdb'...")

    # Kiểm tra container đã tồn tại chưa (kể cả stopped)
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", "name=^/cnosdb$", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )

    if "cnosdb" in result.stdout.strip():
        print("[DOCKER] Container 'cnosdb' đã tồn tại. Đang xóa...")
        subprocess.run(["docker", "rm", "-f", "cnosdb"])

    print("[DOCKER] Đang khởi động container mới...")
    subprocess.run([
        "docker", "run", "--name", "cnosdb", "-p", f"{CNOSDB_PORT}:{CNOSDB_PORT}",
        "-d", "cnosdb/cnosdb:community-latest"
    ])
    time.sleep(5)

    if is_cnosdb_running():
        print("[DOCKER] CnosDB đã khởi động.")
    else:
        print("[DOCKER] Không thể khởi động CnosDB. Kiểm tra Docker.")
        sys.exit(1)

# === CHẠY CẢM BIẾN & DASHBOARD ===
def run_fake_sensor(python_exec):
    """Chạy mô phỏng dữ liệu từ cảm biến."""
    subprocess.run([python_exec, "sensors/run_fake_sensor.py"])

def run_dashboard(python_exec):
    """Chạy giao diện realtime với Streamlit."""
    subprocess.run([os.path.join(os.path.dirname(python_exec), "streamlit"), "run", "ui/dashboard.py"])

# === MAIN ===
def main():
    print("SMART FARM SYSTEM BOOTSTRAP BEGIN")

    # 1. Chuẩn bị môi trường ảo & pip
    python_exec = setup_virtualenv()

    # 2. Khởi động Docker CnosDB
    start_cnosdb_docker()

    # 3. Chạy cảm biến trong nền
    print("[MAIN] Khởi động mô phỏng cảm biến...")
    sensor_thread = threading.Thread(target=run_fake_sensor, args=(python_exec,), daemon=True)
    sensor_thread.start()

    # 4. Đợi vài giây cho có dữ liệu rồi chạy dashboard
    time.sleep(2)
    print("[MAIN] Đang mở dashboard với Streamlit...")
    run_dashboard(python_exec)

if __name__ == "__main__":
    main()
