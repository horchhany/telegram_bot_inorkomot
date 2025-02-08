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
    data = UserData.load_users()

    if not data:
        await update.message.reply_text("No user data found. Please register first.")
        return

    current_index = context.user_data.get("current_index", 0)

    if current_index >= len(data):
        await update.message.reply_text("No more users to display.")
        context.user_data["current_index"] = 0  # Restart browsing
        return

    user_data = data[current_index]
    media_files = user_data.get("media_files", [])

    if user_input == "❤️":
        if media_files:
            media_group = []
            for media in media_files[:10]:  # Max 10 media files
                if media["file_type"] == "photo":
                    media_group.append(InputMediaPhoto(media["file_id"]))
                elif media["file_type"] == "video":
                    media_group.append(InputMediaVideo(media["file_id"]))

            if len(media_group) == 1:
                await context.bot.send_photo(chat_id=chat_id, photo=media_group[0].media)
            else:
                await context.bot.send_media_group(chat_id=chat_id, media=media_group)
        else:
            await update.message.reply_text("No media found.")

        context.user_data["current_index"] = current_index + 1

    elif user_input == "💤":
        await update_user(update, context)  # Restart the conversation
