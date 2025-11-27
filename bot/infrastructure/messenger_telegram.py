import json
import urllib.request
import os
from dotenv import load_dotenv

from bot.domain.messenger import Messenger

load_dotenv()


class MessengerTelegram(Messenger):
    def _get_telegram_base_uri(self) -> str:
        return f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}"

    def makeRequest(self, method: str, **param) -> list[dict]:
        json_data = json.dumps(param).encode("utf-8")

        request = urllib.request.Request(
            method="POST",
            url=f"{self._get_telegram_base_uri()}/{method}",
            data=json_data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            response_json = json.loads(response_body)
            assert response_json["ok"]
            return response_json["result"]

    def getUpdates(self, **params) -> list[dict]:
        return self.makeRequest("getUpdates", **params)

    def sendMessage(self, chat_id: int, text: str, **params) -> list[dict]:
        return self.makeRequest("sendMessage", chat_id=chat_id, text=text, **params)

    def answerCallbackQuery(self, callback_query_id: str, **kwargs) -> dict:
        return self.makeRequest(
            "answerCallbackQuery", callback_query_id=callback_query_id, **kwargs
        )

    def deleteMessage(self, chat_id: int, message_id: int) -> dict:
        return self.makeRequest("deleteMessage", chat_id=chat_id, message_id=message_id)
