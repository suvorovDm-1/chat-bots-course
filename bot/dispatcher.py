from bot.handler import Handler

class Dispatcher:
    def __init__(self):
        self.handlers: list[Handler] = []

    def add_handlers(self, *handlers: list[Handler]) -> None:
        for handler in handlers:
            self.handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        for handler in self.handlers:
            if handler.can_handle(update):
                need_continue = handler.handle(update)
                if not need_continue: break