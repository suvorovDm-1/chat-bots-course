from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage


class DbWriter(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return True

    async def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        await storage.persist_updates(update)
        return HandlerStatus.CONTINUE
