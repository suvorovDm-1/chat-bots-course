import json
import logging
import urllib.request
import os
import time
from dotenv import load_dotenv

from bot.domain.messenger import Messenger

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class MessengerTelegram(Messenger):
    def _get_telegram_base_uri(self) -> str:
        return f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}"

    def makeRequest(self, method: str, **param) -> list[dict]:
        url = f"{self._get_telegram_base_uri()}/{method}"
        start_time = time.time()

        logger.info(f"[HTTP] → POST {method}")

        json_data = json.dumps(param).encode("utf-8")

        request = urllib.request.Request(
            method="POST",
            url=url,
            data=json_data,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request) as response:
                response_body = response.read().decode("utf-8")
                response_json = json.loads(response_body)

                duration_ms = (time.time() - start_time) * 1000
                logger.info(f"[HTTP] ← POST {method} - {duration_ms:.2f}ms")

                return response_json["result"]
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"[HTTP] ✗ POST {method} - {duration_ms:.2f}ms - Error: {e}")
            raise

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
