"""
The bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
Send /cancel to stop the conversation.
"""
import re
import requests
from requests.exceptions import RequestException

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from decouple import config

from chatbot.states import cancel, check_photo, STATES
from chatbot.inputs import FALSE, TRUE

BOT_URL = f"https://api.telegram.org/bot{config('TELEGRAM_BOT_TOKEN')}"


def main() -> None:
    """Run the bot."""
    # Create the Application
    application = Application.builder().token(config("TELEGRAM_BOT_TOKEN")).build()

    # Construct regular expression to match accepted inputs
    regex_str = f"^({'|'.join(TRUE + FALSE)})$"
    regex_pattern = re.compile(regex_str, re.IGNORECASE)

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", check_photo)],
        states={
            STATES.CHECK_PHOTO: [
                MessageHandler(filters.Regex(regex_pattern), check_photo)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
