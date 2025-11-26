import json

from bot.dispatcher import Dispatcher
from bot.handlers.pizza_selection import PizzaSelection

from tests.mock import Mock


def test_pizza_selection_handler():
    # апдейт c callback'ом выбора пиццы
    test_update = {
        "update_id": 123456790,
        "callback_query": {
            "id": "cbq-id-1",
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser",
            },
            "message": {
                "message_id": 10,
                "chat": {
                    "id": 12345,
                    "first_name": "Test",
                    "username": "testuser",
                    "type": "private",
                },
                "date": 1640995201,
                "text": "Please choose pizza name",
            },
            "data": "pizza_margherita",
        },
    }

    update_user_order_called = False
    update_user_state_called = False
    answer_callback_called = False
    delete_message_called = False
    send_message_calls = []

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return {"state": "WAIT_FOR_PIZZA_NAME", "order_json": "{}"}

    def update_user_order(telegram_id: int, order: dict) -> None:
        nonlocal update_user_order_called
        assert telegram_id == 12345

        assert order == {"pizza_name": "Margherita"}
        update_user_order_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        nonlocal update_user_state_called
        assert telegram_id == 12345

        assert state == "WAIT_FOR_PIZZA_SIZE"
        update_user_state_called = True

    def answerCallbackQuery(callback_query_id: str, **kwargs) -> dict:
        nonlocal answer_callback_called
        assert callback_query_id == "cbq-id-1"
        answer_callback_called = True
        return {"ok": True}

    def deleteMessage(chat_id: int, message_id: int, **kwargs) -> dict:
        nonlocal delete_message_called
        assert chat_id == 12345
        assert message_id == 10
        delete_message_called = True
        return {"ok": True}

    def sendMessage(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    mock_storage = Mock(
        {
            "get_user": get_user,
            "update_user_order": update_user_order,
            "update_user_state": update_user_state,
        }
    )
    mock_messenger = Mock(
        {
            "answerCallbackQuery": answerCallbackQuery,
            "deleteMessage": deleteMessage,
            "sendMessage": sendMessage,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(PizzaSelection())

    dispatcher.dispatch(test_update)

    assert update_user_order_called
    assert update_user_state_called
    assert answer_callback_called
    assert delete_message_called

    assert len(send_message_calls) == 1
    assert send_message_calls[0]["text"] == "Please select pizza size"
