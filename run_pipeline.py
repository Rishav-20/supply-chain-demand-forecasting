import sqlite3
import pandas as pd
import os
import sys

DB_PATH = "m5_forecasting.db"
DDL_PATH = "sql_scripts/01_create_tables.sql"
CALENDAR_PATH = "data_raw/calendar.csv"
PRICES_PATH = "data_raw/sell_prices.csv"
SALES_PATH = "data_processed/sales_unpivoted.csv"

print("[*] Rebuilding clean database...")
if os.path.exists(DB_PATH):
    try: os.remove(DB_PATH)
    except: pass

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(DDL_PATH, "r") as f:
    cursor.executescript(f.read())

# THE FIX: Turn off Foreign Keys during massive bulk inserts to prevent constraint crashes
cursor.execute("PRAGMA foreign_keys = OFF;")
cursor.execute("PRAGMA journal_mode = WAL;")
cursor.execute("PRAGMA synchronous = OFF;")

def stream_csv_to_sql(file_path, table_name, chunk_driven=False):
    print(f"[*] Activating data stream for table: '{table_name}'")
    
    # Exclude the auto-increment ID from pandas mapping so SQLite can generate it
    cursor.execute(f"PRAGMA table_info({table_name});")
    sql_columns = [row[1] for row in cursor.fetchall() if row[1] != 'sales_id']

    if chunk_driven:
        chunk_size = 500000
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            chunk.columns = [col.strip() for col in chunk.columns]
            chunk = chunk.rename(columns={'d': 'date_id', 'sales': 'units_sold', 'value': 'units_sold'})
            
            # THE CORE FIX: Drop the Kaggle string ID to avoid the Integer type conflict
            if 'id' in chunk.columns:
                chunk = chunk.drop(columns=['id'])
                
            chunk = chunk[[col for col in chunk.columns if col in sql_columns]]
            chunk.to_sql(table_name, conn, if_exists="append", index=False)
            sys.stdout.write(f"\r    --> Writing Batch {i + 1} ({((i + 1) * chunk_size):,} rows saved)")
            sys.stdout.flush()
        print(f"\n[+] Table '{table_name}' completed!\n")
    else:
        df = pd.read_csv(file_path)
        df.columns = [col.strip() for col in df.columns]
        if table_name == "dim_calendar":
            df = df.rename(columns={'date': 'calendar_date', 'weekday': 'weekday_name', 'wday': 'weekday_int', 'month': 'month_id', 'year': 'year_id'})
        df = df[[col for col in df.columns if col in sql_columns]]
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"[+] Table '{table_name}' completed!\n")

try:
    stream_csv_to_sql(CALENDAR_PATH, "dim_calendar", chunk_driven=False)
    stream_csv_to_sql(PRICES_PATH, "dim_sell_prices", chunk_driven=False)
    stream_csv_to_sql(SALES_PATH, "fact_sales", chunk_driven=True)

    conn.commit()
    print("=== SUCCESS: Database Ingestion Phase is Complete! ===")
except Exception as e:
    print(f"\n[-] Ingestion halted due to error: {e}")
finally:
    conn.close()