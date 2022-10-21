from pydantic import BaseModel


class Command(BaseModel):
    pass


class LocationSearchCommand(Command):
    address: str
