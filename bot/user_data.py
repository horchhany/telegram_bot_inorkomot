import json
import os

class UserData:
    FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "user_data.json")

    @classmethod
    def load_data(cls):
        if os.path.exists(cls.FILE_PATH):
            try:
                with open(cls.FILE_PATH, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def save_user(cls, chat_id, user_data):
        data = cls.load_data()
        for entry in data:
            if entry["chat_id"] == chat_id:
                entry.update(user_data)
                break
        else:
            user_data["chat_id"] = chat_id
            data.append(user_data)
        
        cls.save_data(data)
