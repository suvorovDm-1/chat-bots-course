import bot.db_client
from bot.handlers.handler import Handler, HandlerStatus

class EnsureUserExists(Handler):
    def can_handle(self, update: dict) -> bool:
        # This handler should run for any update that has a user ID
        return "message" in update and "from" in update["message"]

    def handle(self, update: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        # Ensure user exists (check and create if needed in single transaction)
        bot.db_client.ensure_user_exists(telegram_id)

        # Continue processing with other handlers
        return HandlerStatus.CONTINUE