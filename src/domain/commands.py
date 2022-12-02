from pydantic import BaseModel
from typing import Optional


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


class TripGetCommand(Command):
    id: str


class TripGetForDriver(Command):
    driver_username: Optional[str]
    trip_state: Optional[str]
    offset: Optional[int]
    limit: Optional[int]


class TripUpdateCommand(Command):
    trip_id: str
    driver_username: str
    driver_latitude: float
    driver_longitude: float
    trip_state: str
