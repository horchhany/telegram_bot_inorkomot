import os
import psycopg2 # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id BIGINT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    description TEXT,
    media_file_ids TEXT[]
);
""")
conn.commit()


