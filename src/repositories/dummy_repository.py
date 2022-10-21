from src.repositories import BaseRepository


class DummyRepository(BaseRepository):
    def __init__(self):
        pass

    def save(self):
        pass

    def update(self):
        pass
