from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def start_keyboard():
    return ReplyKeyboardMarkup([["Let's Start"]], resize_keyboard=True)

def play_keyboard():
    return ReplyKeyboardMarkup([["❤️", "📩 / 📹", "👎", "💤"]], resize_keyboard=True)

def gender_keyboard():
    return ReplyKeyboardMarkup([["Male", "Female", "Other"]], resize_keyboard=True)

def remove_keyboard():
    return ReplyKeyboardRemove()

# Start command
async def update_user(update, context):
    # Define the keyboard with the "Update information" button
    keyboard = [
        ["1", "2", "3", "4"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Send a message with the "Update information" button
    await update.message.reply_text(
        "Your information!\n1.Profile\n2.Update your profile\n 3.\n 4.\n",
        reply_markup=reply_markup
    )
