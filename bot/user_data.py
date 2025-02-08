import psycopg2 # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class UserData:

    @classmethod
    def save_user(cls, chat_id, user_data):
        """ Saves or updates a user and stores media in `user_media` table. """
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn:
                with conn.cursor() as cursor:
                    # Check if user exists
                    cursor.execute("SELECT 1 FROM users WHERE chat_id = %s", (chat_id,))
                    exists = cursor.fetchone()

                    if exists:
                        # Update user info
                        cursor.execute("""
                            UPDATE users 
                            SET name = %s, age = %s, gender = %s, description = %s
                            WHERE chat_id = %s
                        """, (
                            user_data.get("name"),
                            user_data.get("age"),
                            user_data.get("gender"),
                            user_data.get("description"),
                            chat_id
                        ))
                    else:
                        # Insert new user
                        cursor.execute("""
                            INSERT INTO users (chat_id, name, age, gender, description) 
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            chat_id,
                            user_data.get("name"),
                            user_data.get("age"),
                            user_data.get("gender"),
                            user_data.get("description")
                        ))

                    # Save media files in user_media
                    media_files = user_data.get("media_file_ids", [])

                    if media_files:
                        # Delete old media files for this user
                        cursor.execute("DELETE FROM user_media WHERE chat_id = %s", (chat_id,))
                        
                        # Insert new media files with correct type
                        for media in media_files:
                            cursor.execute("""
                                INSERT INTO user_media (chat_id, file_id, file_type)
                                VALUES (%s, %s, %s)
                            """, (chat_id, media["file_id"], media["file_type"]))

        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()


@classmethod
def load_users(cls):
    """Loads all users from the database and retrieves their media files."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn:
            with conn.cursor() as cursor:
                # Fetch all users
                cursor.execute("SELECT chat_id, name, age, gender, description FROM users")
                users = cursor.fetchall()

                # Fetch media files
                cursor.execute("SELECT chat_id, file_id, file_type FROM user_media")
                media_records = cursor.fetchall()

                # Organize media files by chat_id
                media_dict = {}
                for chat_id, file_id, file_type in media_records:
                    if chat_id not in media_dict:
                        media_dict[chat_id] = []
                    media_dict[chat_id].append({"file_id": file_id, "file_type": file_type})

                # Build user list
                user_list = [
                    {
                        "chat_id": user[0],
                        "name": user[1],
                        "age": user[2],
                        "gender": user[3],
                        "description": user[4],
                        "media_files": media_dict.get(user[0], [])  # Attach user's media
                    }
                    for user in users
                ]

        return user_list

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        conn.close()
