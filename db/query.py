from cnosdb_connector import connect
import pandas as pd
from config.cnosdb_config import CNOSDB_CONFIG

def query_latest_data(limit: int = 5) -> pd.DataFrame:
    try:
        conn = connect(
            url=f"http://{CNOSDB_CONFIG['host']}:{CNOSDB_CONFIG['port']}/",
            user=CNOSDB_CONFIG['user'],
            password=CNOSDB_CONFIG['password']
        )
        conn.switch_database(CNOSDB_CONFIG['database'])

        df = pd.read_sql(f"SELECT * FROM smart_farm ORDER BY time DESC LIMIT {limit}", conn)

        return df  # Trả về DataFrame luôn

    except Exception as e:
        print(f"[ERROR] Query thất bại: {e}")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu lỗi

if __name__ == "__main__":
    print(query_latest_data())
