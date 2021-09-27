import logging
import os

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intent_functions import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.chat_id = os.getenv('SESSION_ID')
        self.tg_bot = os.getenv('BOT_TOKEN')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, bot):
    update.message.reply_text('Здравствуйте!')


def send_tg_messages(update, bot):
    text = detect_intent_texts(
        os.getenv("PROJECT_ID"),
        os.getenv('SESSION_ID'),
        update.message.text)
    if not text.query_result.intent.is_fallback:
        update.message.reply_text(text.query_result.fulfillment_text)
    else:
        update.message.reply_text(
            'К сожалению, бот не знает ответа на ваш вопрос. Вы будете переведены на оператора техподдержки')


def main():
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, send_tg_messages))
    logger.addHandler(TelegramLogsHandler())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
