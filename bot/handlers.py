import os
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
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
    photo = update.message.photo[-1]  # Get highest resolution
    file_id = photo.file_id  # Get the file ID

    context.user_data["photo_url"] = file_id  # Save file_id in user data
    chat_id = update.effective_chat.id

    UserData.save_user(chat_id, context.user_data)  # Save to DB

    await update.message.reply_text(f"Thank you! Your profile is saved.\nName: {context.user_data['name']}")
    return ConversationHandler.END

async def send_saved_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = UserData.load_user(chat_id)

    if user and user.get("photo_url"):
        await context.bot.send_photo(chat_id=chat_id, photo=user["photo_url"])
    else:
        await update.message.reply_text("No photo found.")


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Canceled. Type /start to restart.", reply_markup=remove_keyboard())
    return ConversationHandler.END
