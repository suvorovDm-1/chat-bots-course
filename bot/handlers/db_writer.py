from bot.handlers.handler import Handler, HandlerStatus
from bot.db_client import persist_updates

class DbWriter(Handler):
    def can_handle(self, update: dict) -> bool:
        return True

    def handle(self, update:dict) -> bool:
        persist_updates(update)
        return HandlerStatus.CONTINUE