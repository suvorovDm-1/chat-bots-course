import json
import asyncio

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class PizzaDrinks(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    async def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]
        callback_query_id = update["callback_query"]["id"]

        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_water": "Water",
            "drink_iced_tea": "Iced Tea",
            "drink_none": "No drinks",
        }
        selected_drink = drink_mapping.get(callback_data)

        data["drink"] = selected_drink

        await storage.update_user_order(telegram_id, data)
        await storage.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")

        await asyncio.gather(
            messenger.answerCallbackQuery(callback_query_id),
            messenger.deleteMessage(chat_id=chat_id, message_id=message_id),
        )

        pizza_name = data.get("pizza_name", "Unknown")
        pizza_size = data.get("pizza_size", "Unknown")
        drink = data.get("drink", "Unknown")

        order_summary = f"""🍕 **Your Order Summary:**

**Pizza:** {pizza_name}
**Size:** {pizza_size}
**Drink:** {drink}

Is everything correct?"""

        await messenger.sendMessage(
            chat_id=chat_id,
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Ok", "callback_data": "order_approve"},
                            {
                                "text": "🔄 Start again",
                                "callback_data": "order_restart",
                            },
                        ],
                    ],
                },
            ),
        )

        return HandlerStatus.STOP
