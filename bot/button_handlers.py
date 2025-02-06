
import json
from buttons import update_user
from user_data import UserData


# Retrieve the username based on chat_id
async def get_username_by_chat_id(context, chat_id):
    try:
        # Get chat information using the chat_id
        chat = await context.bot.get_chat(chat_id)
        # Get the username from the chat information
        username = chat.username if chat.username else "No username available"
        return username
    except Exception as e:
        print(f"Error retrieving username for chat_id {chat_id}: {e}")
        return "Error retrieving username"
    
# Handler for received button clicks
async def handle_buttons(update, context):
    
    user_input = update.message.text
    chat_id = update.effective_chat.id

    # Fetch users from PostgreSQL instead of user_data.json
    data = UserData.load_users()

    if not data:
        await update.message.reply_text("No user data found. Please register first.")
        return

    # Initialize the user index
    if user_input in ["❤️", "👎"]:
        current_index = context.user_data.get("current_index", 0)

        if current_index >= len(data):
            await update.message.reply_text("No more users to display.")
            current_index = 0  # Restart the user browsing

        user_data = data[current_index]
        
        # Construct caption
        caption = f"{user_data.get('name', 'No name')}, {user_data.get('age', 'No age')}, {user_data.get('gender', 'No gender')}, {user_data.get('description', 'No description')}"

        # Send user profile
        if user_data.get("photo_url"):
            await context.bot.send_photo(chat_id=chat_id, photo=user_data["photo_url"], caption=caption)
        else:
            await update.message.reply_text(f"No photo found for {user_data['name']}.")

        # Update the index to show the next user
        context.user_data["current_index"] = current_index + 1

    elif user_input == "💤":
        await update_user(update, context)  # Restart the conversation
