from bot.handler import Handler
import bot.tg_client

class PhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]

    def handle(self, update: dict) -> bool:
        chat_id = update["message"]["chat"]["id"]
        file_id = update["message"]["photo"][-1]["file_id"]
        bot.tg_client.sendPhoto(chat_id=chat_id, photo=file_id)
        return False