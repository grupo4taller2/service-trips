from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.conf import config

from src.repositories import TripRepository
from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork


engine = create_engine(
        config.Settings().DATABASE_URI,
        isolation_level="REPEATABLE READ",
    )

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=engine
)


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.trip_repository = TripRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
