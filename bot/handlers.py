import json
from telegram import Update # type: ignore
from telegram.ext import CallbackContext, ConversationHandler # type: ignore
from user_data import UserData
from buttons import start_keyboard, play_keyboard, gender_keyboard, remove_keyboard

NAME, AGE, GENDER, DESCRIPTION, PHOTO = range(5)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the bot! Click 'Let's Start' to begin.", reply_markup=start_keyboard())

async def play(update: Update, context: CallbackContext):
    await update.message.reply_text("Click below button to review.", reply_markup=play_keyboard())

async def lets_start(update: Update, context: CallbackContext):
    await update.message.reply_text("Great! What's your name?", reply_markup=remove_keyboard())
    return NAME

async def ask_age(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(f"Hi {context.user_data['name']}! How old are you?")
    return AGE

async def ask_gender(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("What is your gender?", reply_markup=gender_keyboard())
    return GENDER

async def ask_description(update: Update, context: CallbackContext):
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("Tell me about yourself.")
    return DESCRIPTION

async def ask_photo(update: Update, context: CallbackContext):
    context.user_data["description"] = update.message.text
    await update.message.reply_text("Please upload a photo.")
    return PHOTO

async def finish(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    media_file_ids = []

    # Check if the user sent multiple photos
    if update.message.photo:
        for photo in update.message.photo:
            file = await photo.get_file()
            media_file_ids.append(file.file_id)  # Store the file_id, not the local path

    # Check if the user sent a video
    if update.message.video:
        file = await update.message.video.get_file()
        media_file_ids.append(file.file_id)

    if not media_file_ids:
        await update.message.reply_text("Please send at least one photo or video.")
        return

    # Save media file IDs in user data
    context.user_data["media_file_ids"] = media_file_ids
    UserData.save_user(chat_id, context.user_data)

    await update.message.reply_text(f"Thank you! Your profile is saved with {len(media_file_ids)} media files.")
    return ConversationHandler.END



async def send_user_media(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data = UserData.load_user(chat_id)

    if not user_data or not user_data.get("media_file_ids"):
        await update.message.reply_text("No media found for this user.")
        return

    for file_id in user_data["media_file_ids"]:
        await context.bot.send_photo(chat_id=chat_id, photo=file_id)

    await update.message.reply_text("Here are your saved media files.")


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Canceled. Type /start to restart.", reply_markup=remove_keyboard())
    return ConversationHandler.END
