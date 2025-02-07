from db import conn, cursor

class UserData:

    @classmethod
    def save_user(cls, chat_id, user_data):
        cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
        existing_user = cursor.fetchone()

        media_file_ids = user_data.get("media_file_ids", [])

        if existing_user:
            cursor.execute("""
                UPDATE users 
                SET name = %s, age = %s, gender = %s, description = %s, media_file_ids = %s
                WHERE chat_id = %s
            """, (user_data.get("name"), user_data.get("age"), user_data.get("gender"), 
                  user_data.get("description"), media_file_ids, chat_id))
        else:
            cursor.execute("""
                INSERT INTO users (chat_id, name, age, gender, description, media_file_ids) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (chat_id, user_data.get("name"), user_data.get("age"), user_data.get("gender"), 
                  user_data.get("description"), media_file_ids))
        
        conn.commit()

    @classmethod
    def load_users(cls):
        cursor.execute("SELECT chat_id, name, age, gender, description, media_file_ids FROM users")
        users = cursor.fetchall()

        user_list = []
        for user in users:
            user_list.append({
                "chat_id": user[0],
                "name": user[1],
                "age": user[2],
                "gender": user[3],
                "description": user[4],
                "media_file_ids": user[5]  # This is the Telegram file_id
            })

        return user_list
