import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler
)
from chatbot.handlers import (
    start,
    help_command,
    message_handler,
    new_command_handler,
    SYSTEM_PROMPT_SP,
    CANCEL_SP
)
from chatbot.filters import AuthFilter, MessageFilter
from dotenv import load_dotenv

load_dotenv()


def start_bot():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start, filters=AuthFilter))
    app.add_handler(CommandHandler("help", help_command, filters=AuthFilter))
    app.add_handler(CommandHandler("new", new_command_handler, filters=AuthFilter))
    app.add_handler(MessageHandler(MessageFilter, message_handler))

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)