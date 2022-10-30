from __future__ import annotations
from typing import Union

from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import TripFacade
from src.domain.rider import Rider
from src.domain.location import Location
from src.domain.directions import Directions
from src.domain.time import Time
from src.domain.distance import Distance
from src.utils.formatters import DistanceFormatter, TimeFormatter


Base = declarative_base()


class RequestedTripDTO(Base):
    __tablename__ = 'requested_trips'
    id: Union[str, Column] = Column(String, primary_key=True)
    state: Union[str, Column] = Column(String)
    rider_username: Union[str, Column] = Column(String,
                                                unique=True,
                                                index=True)
    origin_address: Union[str, Column] = Column(String)
    origin_latitude: Union[float, Column] = Column(Float)
    origin_longitude: Union[float, Column] = Column(Float)
    destination_address: Union[str, Column] = Column(String)
    destination_latitude: Union[float, Column] = Column(Float)
    destination_longitude: Union[float, Column] = Column(Float)
    estimated_time: Union[int, Column] = Column(Integer)
    type: Union[str, Column] = Column(String)
    estimated_price: Union[float, Column] = Column(Float)
    distance: Union[int, Column] = Column(Integer)
    created_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    def from_entity(trip: Trip) -> RequestedTripDTO:
        return RequestedTripDTO(
            id=trip.id,
            state=trip.state.name,
            rider_username=trip.rider.username,
            origin_address=trip.directions.origin.address,
            origin_latitude=trip.directions.origin.latitude,
            origin_longitude=trip.directions.origin.longitude,
            destination_address=trip.directions.destination.address,
            destination_latitude=trip.directions.destination.latitude,
            destination_longitude=trip.directions.destination.longitude,
            estimated_time=trip.directions.time.seconds,
            type=trip.type,
            estimated_price=trip.estimated_price,
            distance=trip.directions.distance.meters
        )

    def to_entity(self) -> Trip:
        rider = Rider(self.rider_username)
        origin = Location(self.origin_address,
                          self.origin_latitude,
                          self.origin_longitude)
        destination = Location(self.destination_address,
                               self.destination_latitude,
                               self.destination_longitude)
        time = Time(self.estimated_time,
                    TimeFormatter().format(self.estimated_time))
        distance = Distance(self.distance,
                            DistanceFormatter().format(self.distance))
        directions = Directions(origin,
                                destination,
                                time,
                                distance)

        return Trip(
            id=self.id,
            rider=rider,
            directions=directions,
            type=self.type,
            state=TripFacade().create_from_name(self.state),
            estimated_price=self.estimated_price
        )
