from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork


class DummyUnitOfWork(AbstractUnitOfWork):

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def collect_new_events(self):
        return []
