from buttons import update_user
from user_data import UserData
from telegram import InputMediaPhoto, InputMediaVideo  # type: ignore

# Retrieve the username based on chat_id
async def get_username_by_chat_id(context, chat_id):
    try:
        chat = await context.bot.get_chat(chat_id)
        return chat.username if chat.username else "No username available"
    except Exception as e:
        print(f"Error retrieving username for chat_id {chat_id}: {e}")
        return "Error retrieving username"

# Handler for received button clicks
async def handle_buttons(update, context):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    # Fetch users from PostgreSQL
    users = UserData.load_users()

    if not users:
        await update.message.reply_text("No user data found. Please register first.")
        return

    current_index = context.user_data.get("current_index", 0)

    if current_index >= len(users):
        await update.message.reply_text("No more users to display.")
        context.user_data["current_index"] = 0  # Restart browsing
        return

    user_data = users[current_index]

    # Prepare user information
    name = user_data.get("name", "No name provided")
    age = user_data.get("age", "No age provided")
    gender = user_data.get("gender", "No gender provided")
    description = user_data.get("description", "No description provided")

    username = await get_username_by_chat_id(context, user_data.get("chat_id", chat_id))
    caption = f"{name}, @{username}, {age}, {gender}, {description}"

    # Fetch media files from database
    media_files = user_data.get("media_files", [])

    if user_input == "❤️":
        if media_files:
            media_group = []

            for media in media_files[:10]:  # Max 10 files
                file_id = media.get("file_id")
                file_type = media.get("file_type", "photo")  # Default to photo

                if file_type == "photo":
                    media_group.append(InputMediaPhoto(file_id))
                elif file_type == "video":
                    media_group.append(InputMediaVideo(file_id))

            # Send media as a group (if multiple files exist)
            if media_group:
                await context.bot.send_media_group(chat_id=chat_id, media=media_group)

            # Send caption separately
            await update.message.reply_text(caption)

        else:
            await update.message.reply_text(f"No media found for {name}.")

        # Move to the next user
        context.user_data["current_index"] = current_index + 1

    elif user_input == "💤":
        await update_user(update, context)  # Restart the conversation
