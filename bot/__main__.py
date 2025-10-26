import bot.db_client
import bot.tg_client
import time
from bot.dispatcher import Dispatcher
from bot.handlers.message_echo import MessageEcho
from bot.handlers.db_writer import DbWriter
from bot.handlers.photo_echo import PhotoEcho
from bot.long_polling import start_long_polling

if __name__ == "__main__":
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handlers(DbWriter(), MessageEcho(), PhotoEcho())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")