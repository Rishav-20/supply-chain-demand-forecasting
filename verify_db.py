import sqlite3

DB_PATH = "m5_forecasting.db"

print("\n[*] Initializing Database Row Verification Engine...")
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query all custom user tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    print("\n==============================")
    print("      TABLE RECORD COUNTS     ")
    print("==============================")
    
    for table in tables:
        table_name = table[0]
        # Execute row count cleanly
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        print(f"[+] {table_name:<16} : {row_count:,} rows")
        
    print("==============================\n")
    conn.close()

except Exception as e:
    print(f"[-] Database Verification Failed: {e}")