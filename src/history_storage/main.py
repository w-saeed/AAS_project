import os
import sqlite3
import pandas as pd

CSV_FOLDER = '/csv_folder'
DB_PATH = '/sqlite_data/history_storage.sqlite'
TABLE_NAME = 'timeseries_sensors'
TRACK_FILE = '/sqlite_data/processed_files.txt'

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_processed_files():
    if not os.path.exists(TRACK_FILE):
        return set()
    with open(TRACK_FILE, 'r') as f:
        return set(line.strip() for line in f.readlines())

def save_processed_file(filename):
    with open(TRACK_FILE, 'a') as f:
        f.write(filename + '\n')

def ensure_table_exists(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            sensor_id TEXT,
            measurement_type TEXT,
            value REAL,
            epoch_ms TEXT,
            timestamp_iso TEXT,
            PRIMARY KEY (sensor_id, timestamp_iso)
        )
    ''')
    conn.commit()
    conn.close()

def append_csv_to_sqlite(csv_file, db_path, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cols = df.columns.tolist()
    placeholders = ','.join(['?'] * len(cols))
    insert_sql = f"INSERT OR IGNORE INTO {table_name} ({','.join(cols)}) VALUES ({placeholders})"
    cur.executemany(insert_sql, df.values.tolist())
    conn.commit()
    conn.close()

def main():
    ensure_table_exists(DB_PATH, TABLE_NAME)
    processed = get_processed_files()
    files = [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]
    for file in files:
        if file not in processed:
            print(f"Processing {file}")
            append_csv_to_sqlite(os.path.join(CSV_FOLDER, file), DB_PATH, TABLE_NAME)
            save_processed_file(file)

if __name__ == '__main__':
    main()
