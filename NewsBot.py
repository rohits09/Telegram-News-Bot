#                          Telegram News Bot

import logging
from time import sleep
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from DialogFlowInteg import get_reply, fetch_news, Keyboard_Category



logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)



# Access Token for Telegram API Interface
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Runs after user type /start Command in Telegram
def start(update: Update, context: CallbackContext):
    authorName = update.message.from_user.first_name
    reply = f"Hello {authorName}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# Runs after user type /help Command in Telegram
def _help(update, context):
    help_txt = "Hey! How can I Help You"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_txt)

# Runs after user types some text
def reply_text(update, context):
    intent, reply = get_reply(update.message.text, update.effective_chat.id)

    if intent == "GetNews":
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.effective_chat.id, text=article["link"])

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def news(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Choose a Category", reply_markup=ReplyKeyboardMarkup(keyboard= Keyboard_Category, one_time_keyboard=True))

# Reply with same Sticker as send by user
def echo_sticker(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=update.message.sticker.file_id)

# For handling all errors
def error(update, context):
    logger.error("Update '%s' caused error '%s'", update, context.error)

# Prevent if user types some unknown/unrelated commands
def unknown(update, context):
    reply="Sorry!!!... Wrong Command."
    context.bot.send_message(chat_id=update.effective_chat.id,
text=reply)

def main():
    # Its a Class: for Recieving updates from telegram server and sends them to dispatcher for handling them.
    updater = Updater(TOKEN, use_context=True)
    sleep(1)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Started Polling ...")

    # Stops when you pressed ctrl+c
    updater.idle()



if __name__ == "__main__":
    main()

