from pydantic import BaseModel


class Command(BaseModel):
    pass


class LocationSearchCommand(Command):
    address: str


class DirectionsSearchCommand(Command):
    origin: str
    destination: str


class TripRequestCommand(Command):
    rider_username: str
    rider_origin_address: str
    rider_destination_address: str
    trip_type: str
