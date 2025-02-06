
import json
from buttons import update_user

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

    # Get the text sent by the user (button text)
    user_input = update.message.text
    if user_input == "❤️":
        chat_id = update.effective_chat.id
        try:
            # Read all entries from user_data.json
            with open("data/user_data.json", "r") as f:
                data = json.load(f)

            if not data:
                await update.message.reply_text("No user data found. Please register first.")
                return
            
            # Initialize or retrieve the counter for "❤️" clicks
            click_count = context.user_data.get("click_count", 0)

            # Check if the user has already clicked "❤️" 10 times
            if click_count >= 10:
                await update.message.reply_text("You've reached the limit of 10 clicks. Please try again later.")
                return
            # Get the current index of the user to show, default to 0 if it's the first click
            current_index = context.user_data.get("current_index", 0)

            # Check if the index is out of bounds (i.e., if all users have been shown)
            if current_index >= len(data):
                await update.message.reply_text("No more users to display.")
                current_index = 0  # Restart the user_input="❤️"

            user_data = data[current_index]

            # Prepare caption with default values if keys are missing
            name = user_data.get("name", "No name provided")
            age = user_data.get("age", "No age provided")
            gender = user_data.get("gender", "No gender provided")
            description = user_data.get("description", "No description provided")

            # Get the username if available
            username = await get_username_by_chat_id(context, user_data.get("chat_id", chat_id))

            # Check if the user's photo exists
            if "photo" in user_data:
                photo_path = user_data["photo"]
            else:
                await update.message.reply_text(f"No photo found for {name}.")
                return  # If no photo, don't send anything

            # Construct the caption
            caption = f"{name}, {age}, {gender}, {description}" #@{username},

            # Send the user's photo with the caption
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo_path,  # Path to the user's photo
                caption=caption     # Text to display under the photo
            )

            # Update the index to show the next user next time
            context.user_data["current_index"] = current_index + 1
            # Increment the click count
            context.user_data["click_count"] = click_count + 1

        except FileNotFoundError:
            await update.message.reply_text("User data file not found. Please register first.")
        except json.JSONDecodeError:
            await update.message.reply_text("Error reading user data. Please try again later.")

    elif user_input == "📩 / 📹":
        chat_id = update.effective_chat.id
        try:
            # Read all entries from user_data.json
            with open("data/user_data.json", "r") as f:
                data = json.load(f)

            if not data:
                await update.message.reply_text("No user data found. Please register first.")
                return

            # Get the current index of the user to show, default to 0 if it's the first click
            current_index_view = context.user_data.get("current_index_view", 0)

            # Check if the index is out of bounds (i.e., if all users have been shown)
            if current_index_view >= len(data):
                await update.message.reply_text("No more users to display.")
                current_index_view = 0  # Restart the user_input="❤️"

            # Get the user data for the current index
            user_data = data[current_index_view]

            # Prepare caption with default values if keys are missing
            name = user_data.get("name", "No name provided")
            age = user_data.get("age", "No age provided")
            gender = user_data.get("gender", "No gender provided")
            description = user_data.get("description", "No description provided")

            # Get the username if available
            username = await get_username_by_chat_id(context, user_data.get("chat_id", chat_id))

            # Check if the user's photo exists
            if "photo" in user_data:
                photo_path = user_data["photo"]
            else:
                await update.message.reply_text(f"No photo found for {name}.")
                return  # If no photo, don't send anything

            # Construct the caption
            caption = f"{name}, @{username}, {age}, {gender}, {description}" 

            # Send the user's photo with the caption
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo_path,  # Path to the user's photo
                caption=caption     # Text to display under the photo
            )

            # Update the index to show the next user next time
            context.user_data["current_index_view"] = current_index_view + 1

        except FileNotFoundError:
            await update.message.reply_text("User data file not found. Please register first.")
        except json.JSONDecodeError:
            await update.message.reply_text("Error reading user data. Please try again later.")

    elif user_input == "👎":
        #await update.message.reply_text("You pressed 👎. That's disappointing 😢.")
        chat_id = update.effective_chat.id
        try:
            # Read all entries from user_data.json
            with open("data/user_data.json", "r") as f:
                data = json.load(f)

            if not data:
                await update.message.reply_text("No user data found. Please register first.")
                return

            # Get the current index of the user to show, default to 0 if it's the first click
            current_index = context.user_data.get("current_index", 0)

            # Check if the index is out of bounds (i.e., if all users have been shown)
            if current_index >= len(data):
                await update.message.reply_text("No more users to display.")
                current_index = 0  # Restart the user_input="❤️"

            # Get the user data for the current index
            user_data = data[current_index]

            # Prepare caption with default values if keys are missing
            name = user_data.get("name", "No name provided")
            age = user_data.get("age", "No age provided")
            gender = user_data.get("gender", "No gender provided")
            description = user_data.get("description", "No description provided")

            # Get the username if available
            username = await get_username_by_chat_id(context, user_data.get("chat_id", chat_id))

            # Check if the user's photo exists
            if "photo" in user_data:
                photo_path = user_data["photo"]
            else:
                await update.message.reply_text(f"No photo found for {name}.")
                return  # If no photo, don't send anything

            # Construct the caption
            caption = f"{name}, {age}, {gender}, {description}" #@{username},

            # Send the user's photo with the caption
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo_path,  # Path to the user's photo
                caption=caption     # Text to display under the photo
            )

            # Update the index to show the next user next time
            context.user_data["current_index"] = current_index + 1

        except FileNotFoundError:
            await update.message.reply_text("User data file not found. Please register first.")
        except json.JSONDecodeError:
            await update.message.reply_text("Error reading user data. Please try again later.")
        
    elif user_input == "💤":
        #await update.message.reply_text("💤 Time to relax! Goodnight!")
        await update_user(update, context)  # Restart the conversation