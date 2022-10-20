from __future__ import annotations

import abc
from src.repositories.base_repository import BaseRepository


class AbstractUnitOfWork(abc.ABC):
    trip_repository: BaseRepository
    rider_repository: BaseRepository
    driver_repository: BaseRepository
    admin_repository: BaseRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_events(self):
        entities = self.admin_repository.seen
        for e in entities:
            while e.events:
                yield e.events.pop(0)

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
