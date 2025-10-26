from bot.handlers.handler import Handler
from bot.handlers.message_echo import MessageEcho
from bot.handlers.db_writer import DbWriter
from bot.handlers.photo_echo import PhotoEcho

def get_handlers() -> list[Handler]:
    return [
        DbWriter(),
        MessageEcho(),
        PhotoEcho()
    ]