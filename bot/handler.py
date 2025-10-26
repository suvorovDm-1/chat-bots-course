from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def can_handle(self, update:dict) -> bool: ...

    @abstractmethod
    def handle(self, update:dict) -> bool:
        """
        Return value:
        True - if the dispatcher has to continue further processing
        False - if the dispatcher has to stop processing
        """
        pass
