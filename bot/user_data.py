import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class UserData:

    @classmethod
    def save_user(cls, chat_id, user_data):
        """ Saves or updates a user in the database. """
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn:
                with conn.cursor() as cursor:
                    # Check if the user already exists
                    cursor.execute("SELECT 1 FROM users WHERE chat_id = %s", (chat_id,))
                    exists = cursor.fetchone()

                    if exists:
                        # Update user info
                        cursor.execute("""
                            UPDATE users 
                            SET name = %s, age = %s, gender = %s, description = %s, media_file_ids = %s
                            WHERE chat_id = %s
                        """, (
                            user_data.get("name"),
                            user_data.get("age"),
                            user_data.get("gender"),
                            user_data.get("description"),
                            user_data.get("media_file_ids"),  # Stored as an array in PostgreSQL
                            chat_id
                        ))
                    else:
                        # Insert new user
                        cursor.execute("""
                            INSERT INTO users (chat_id, name, age, gender, description, media_file_ids) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            chat_id,
                            user_data.get("name"),
                            user_data.get("age"),
                            user_data.get("gender"),
                            user_data.get("description"),
                            user_data.get("media_file_ids")
                        ))
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    @classmethod
    def load_users(cls):
        """ Loads all users from the database. """
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT chat_id, name, age, gender, description, media_file_ids FROM users")
                    users = cursor.fetchall()

                    user_list = [
                        {
                            "chat_id": user[0],
                            "name": user[1],
                            "age": user[2],
                            "gender": user[3],
                            "description": user[4],
                            "media_file_ids": user[5]  # This is now stored as an array
                        }
                        for user in users
                    ]

            return user_list

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []

        finally:
            conn.close()
