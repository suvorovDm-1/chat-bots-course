import json
import asyncio

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class OrderApproval(Handler):
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

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

    async def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        cq = update["callback_query"]

        telegram_id = cq["from"]["id"]
        callback_data = cq["data"]

        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]
        callback_query_id = cq["id"]

        await asyncio.gather(
            messenger.answerCallbackQuery(callback_query_id),
            messenger.deleteMessage(chat_id=chat_id, message_id=message_id),
        )

        if callback_data == "order_approve":
            await storage.update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = data.get("pizza_name", "Unknown")
            pizza_size = data.get("pizza_size", "Unknown")
            drink = data.get("drink", "Unknown")

            order_confirmation = f"""✅ **Order Confirmed!**
🍕 **Your Order:**
• Pizza: {pizza_name}
• Size: {pizza_size}
• Drink: {drink}

Thank you for your order! Your pizza will be ready soon.

Send /start to place another order."""

            await messenger.sendMessage(
                chat_id=chat_id,
                text=order_confirmation,
                parse_mode="Markdown",
            )

        elif callback_data == "order_restart":
            await storage.clear_user_state_and_order(telegram_id)
            await storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            await messenger.sendMessage(
                chat_id=chat_id,
                text="Please choose pizza type",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Margherita",
                                    "callback_data": "pizza_margherita",
                                },
                                {
                                    "text": "Pepperoni",
                                    "callback_data": "pizza_pepperoni",
                                },
                            ],
                            [
                                {
                                    "text": "Quattro Stagioni",
                                    "callback_data": "pizza_quattro_stagioni",
                                },
                                {
                                    "text": "Capricciosa",
                                    "callback_data": "pizza_capricciosa",
                                },
                            ],
                            [
                                {"text": "Diavola", "callback_data": "pizza_diavola"},
                                {
                                    "text": "Prosciutto",
                                    "callback_data": "pizza_prosciutto",
                                },
                            ],
                        ],
                    }
                ),
            )

        return HandlerStatus.STOP
