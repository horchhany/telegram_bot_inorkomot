import os
import psycopg2  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create 'users' table first
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id BIGINT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    description TEXT
);
""")
conn.commit()

# Create 'user_media' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_media (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    file_id TEXT NOT NULL,
    file_type TEXT CHECK (file_type IN ('photo', 'video')),
    FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE
);
""")
conn.commit()

# Close connection
cursor.close()
conn.close()
