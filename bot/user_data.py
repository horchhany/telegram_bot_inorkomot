from db import conn, cursor

class UserData:
    @classmethod
    def save_user(cls, chat_id, user_data):
        cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute("""
                UPDATE users 
                SET name = %s, age = %s, gender = %s, description = %s, photo_file_id = %s
                WHERE chat_id = %s
            """, (user_data.get("name"), user_data.get("age"), user_data.get("gender"), 
                  user_data.get("description"), user_data.get("photo_file_id"), chat_id))
        else:
            cursor.execute("""
                INSERT INTO users (chat_id, name, age, gender, description, photo_file_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (chat_id, user_data.get("name"), user_data.get("age"), user_data.get("gender"), 
                  user_data.get("description"), user_data.get("photo_file_id")))
        
        conn.commit()

    @classmethod
    def load_users(cls):
        cursor.execute("SELECT chat_id, name, age, gender, description, photo_file_id FROM users")
        users = cursor.fetchall()

        user_list = []
        for user in users:
            user_list.append({
                "chat_id": user[0],
                "name": user[1],
                "age": user[2],
                "gender": user[3],
                "description": user[4],
                "photo_file_id": user[5]  # This is the Telegram file_id
            })

        return user_list
