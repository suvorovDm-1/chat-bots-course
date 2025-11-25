from bot.handlers.handler import Handler
from bot.handlers.db_writer import DbWriter
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart
from bot.handlers.pizza_selection import PizzaSelection
from bot.handlers.pizza_size import PizzaSize

def get_handlers() -> list[Handler]:
    return [
        DbWriter(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelection(),
        PizzaSize(),
    ]