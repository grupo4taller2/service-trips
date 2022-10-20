import abc
from typing import Set, Any


class BaseRepository(metaclass=abc.ABCMeta):
    def __init__(self):
        self.seen: Set[Any] = set()

    @abc.abstractmethod
    def save(self, entity: Any) -> Any:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update(self, entity: Any) -> Any:
        raise NotImplementedError
