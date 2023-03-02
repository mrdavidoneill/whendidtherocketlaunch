"""
This is a module containing functions for Telegram bot conversation handlers for 
checking whether a rocket has taken off from a video. The functions included are:

- get_or_create_bisector: gets or creates a FrameXBisector object from the user_data 
    of the context.
- check_photo: sends a photo and asks the user whether the rocket has taken off. 
    Uses the FrameXBisector object to process the user's response and bisect the
    video to find the frame where the rocket took off.
- cancel: cancels the conversation.

The module uses the logging and telegram libraries for logging and interacting 
with the Telegram API.
"""
from enum import Enum

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from video.bisector import FrameXBisector
from health.log import logger
from chatbot.inputs import TRUE


class STATES(Enum):
    """
    An enumeration of different states for the chatbot.

    Attributes:
    - CHECK_PHOTO: The state when the chatbot is waiting for the user to send a photo.
    """

    CHECK_PHOTO = 0


OPTIONS = ["Yes", "No"]


def get_or_create_bisector(context: ContextTypes.DEFAULT_TYPE):
    """
    Get or create bisector instance from context user data.

    Args:
    - context (telegram.ext.Context): Context in which the message is processed.

    Returns:
    - FrameXBisector: Bisector instance from context user data.
    """
    return context.user_data.setdefault("bisector", FrameXBisector())


async def check_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Sends the photo and asks if rocket has taken off.

    Args:
    - update (telegram.Update): Incoming message from user.
    - context (telegram.ext.Context): Context in which the message is processed.

    Returns:
    - int: ConversationHandler.END if the bisector is finished; otherwise, STATES.CHECK_PHOTO.
    """

    bisector = get_or_create_bisector(context)
    logger.info("%s input: %s", update.message.from_user, update.message.text)

    # Process user input
    if update.message.text == "/start":
        logger.info("Video with %s frames", bisector.count)
    else:
        bisector.process_input(update.message.text.lower() in TRUE)

    if bisector.is_finished:
        # Get found index
        bisector.go_to_mid()
        logger.info("Takeoff happened at frame %s", bisector.index)

        await update.message.reply_text(
            f"Takeoff happened at frame {bisector.index}!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await context.bot.send_photo(update.message.chat.id, bisector.image)
        bisector.reset()
        return ConversationHandler.END

    # Run bisector
    bisector.go_to_mid()
    logger.info(
        "Testing %s in [%s : %s]", bisector.index, bisector.left, bisector.right
    )

    # Show mid frame to user
    await context.bot.send_photo(update.message.chat.id, bisector.image)
    # Ask user if rocket has taken off
    await update.message.reply_text(
        "Has the rocket taken off?",
        reply_markup=ReplyKeyboardMarkup(
            [OPTIONS],
            input_field_placeholder=f"{' or '.join(OPTIONS)}?",
        ),
    )

    return STATES.CHECK_PHOTO


async def cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels and ends the conversation.

    Args:
    - update (telegram.Update): Incoming message from user.
    - context (telegram.ext.Context): Context in which the message is processed.

    Returns:
    - int: ConversationHandler.END to signal the end of the conversation.
    """
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
