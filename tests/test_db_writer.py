import pytest

from bot.dispatcher import Dispatcher
from bot.handlers.db_writer import DbWriter
from tests.mock import Mock


@pytest.mark.asyncio
async def test_database_writer_execution():
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser",
            },
            "chat": {
                "id": 12345,
                "first_name": "Test",
                "username": "testuser",
                "type": "private",
            },
            "date": 1640995200,
            "text": "Hello, this is a test message",
        },
    }

    persist_update_called = False

    async def persist_updates(update: dict) -> None:
        nonlocal persist_update_called
        persist_update_called = True
        assert update == test_update

    async def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return None

    mock_storage = Mock(
        {
            "persist_updates": persist_updates,
            "get_user": get_user,
        }
    )
    mock_messenger = Mock({})

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(DbWriter())

    await dispatcher.dispatch(test_update)

    assert persist_update_called
