import sqlite3

conn = sqlite3.connect("main.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

cursor.execute("""CREATE TABLE IF NOT EXISTS economy(
    id INTEGER PRIMARY KEY,
    name TEXT,
    wallet INTEGER DEFAULT 0,
    bank INTEGER DEFAULT 0
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS poll(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    guild TEXT,
    channel TEXT,
    message TEXT,
    ended BOOLEAN DEFAULT FALSE,
    options TEXT,
    results BLOB
)""")

conn.commit()