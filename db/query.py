from cnosdb_connector import connect
from config.cnosdb_config import CNOSDB_CONFIG
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd


def get_connection():
    return connect(
        url=f"http://{CNOSDB_CONFIG['host']}:{CNOSDB_CONFIG['port']}/",
        user=CNOSDB_CONFIG['user'],
        password=CNOSDB_CONFIG['password']
    )


def get_station_list() -> list[str]:
    try:
        conn = get_connection()
        conn.switch_database(CNOSDB_CONFIG['database'])
        result = conn.execute("SELECT DISTINCT station FROM smart_farm")
        df = pd.DataFrame(result)
        return sorted(df['station'].dropna().unique().tolist())
    except Exception as e:
        print(f"[ERROR] Không thể lấy danh sách vùng: {e}")
        return []


def query_station_data(station: str, limit: int = 1000) -> pd.DataFrame:
    try:
        conn = get_connection()
        conn.switch_database(CNOSDB_CONFIG['database'])

        query = f"""
        SELECT * FROM smart_farm 
        WHERE station = '{station}' 
        ORDER BY time DESC LIMIT {limit}
        """
        result = conn.execute(query)
        df = pd.DataFrame(result)
        df['station'] = station
        return df
    except Exception as e:
        print(f"[ERROR] Truy vấn thất bại cho '{station}': {e}")
        return pd.DataFrame()


from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

def query_multiple_stations(
    stations: list[str], 
    limit: int = 1000,
    max_workers: int = 32
) -> pd.DataFrame:
    """
    Truy vấn dữ liệu từ nhiều station song song, mỗi station lấy tối đa `limit` bản ghi.

    Args:
        stations (list[str]): Danh sách tên các station.
        limit (int): Số bản ghi tối đa mỗi station.
        max_workers (int): Số luồng xử lý song song (mặc định 32).

    Returns:
        pd.DataFrame: Kết quả gộp dữ liệu của tất cả station.
    """
    dfs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(query_station_data, station, limit): station
            for station in stations
        }
        for future in as_completed(futures):
            try:
                df = future.result()
                if not df.empty:
                    dfs.append(df)
            except Exception as e:
                station = futures[future]
                print(f"[ERROR] Lỗi khi xử lý station '{station}': {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
