from bot.handlers.handler import Handler
from bot.handlers.message_echo import MessageEcho
from bot.handlers.db_writer import DbWriter
from bot.handlers.photo_echo import PhotoEcho
from bot.handlers.ensure_user_exists import EnsureUserExists

def get_handlers() -> list[Handler]:
    return [
        DbWriter(),
        EnsureUserExists(),
        MessageEcho(),
        PhotoEcho()
    ]