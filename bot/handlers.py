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
    photo = update.message.photo[-1]
    file_id = photo.file_id  # Get the file_id from Telegram
    chat_id = update.effective_chat.id

    context.user_data["photo_file_id"] = file_id  
    UserData.save_user(chat_id, context.user_data)  # Save to PostgreSQL

    await update.message.reply_text(f"Thank you! Your profile is saved.\nName: {context.user_data['name']}")
    return ConversationHandler.END


async def send_saved_photo(update: Update, context: CallbackContext):
    # Fetch user data from PostgreSQL
    user_data = UserData.load_user(chat_id)
    photo_file_id = user_data.get("photo_file_id")

    # Send photo using Telegram's file_id
    if photo_file_id:
        await context.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=caption)
    else:
        await update.message.reply_text(f"No photo found for {name}.")



async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Canceled. Type /start to restart.", reply_markup=remove_keyboard())
    return ConversationHandler.END
