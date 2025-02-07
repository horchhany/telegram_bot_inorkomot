import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler # type: ignore
from handlers import start, lets_start, ask_age, ask_gender, ask_description, ask_photo, finish, cancel, play
from config import TOKEN
from handlers import NAME, AGE, GENDER, DESCRIPTION, PHOTO
from button_handlers import handle_buttons

logging.basicConfig(level=logging.INFO)

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Let's Start$"), lets_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gender)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_description)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_photo)],
            PHOTO: [MessageHandler(filters.PHOTO, finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(conv_handler)
    # Add message handler for button clicks
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,  handle_buttons))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
