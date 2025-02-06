import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE users DROP COLUMN IF EXISTS photo_url;


""")
conn.commit()

