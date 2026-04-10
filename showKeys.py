import sqlite3

DB_FILE = "database/api_keys.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM api_key")
    rows = cursor.fetchall()

    if not rows:
        print("No API keys found in database")
    else:
        column_names = [description[0] for description in cursor.description]
        print(" | ".join(column_names))

        for row in rows:
            print(" | ".join(str(value) for value in row))

except sqlite3.Error as e:
    print(f"Database error: {e}")

conn.close()