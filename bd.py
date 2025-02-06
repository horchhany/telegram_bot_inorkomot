from bot.db import conn, cursor
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id BIGINT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    description TEXT,
    photo_url TEXT
);
""")
conn.commit()
