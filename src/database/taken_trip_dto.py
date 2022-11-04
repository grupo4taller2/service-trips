from __future__ import annotations
from typing import Union

from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

from src.domain.trips.trip import Trip

Base = declarative_base()


class TakenTripDTO(Base):
    __tablename__ = 'taken_trips'
    id: Union[str, Column] = Column(String, primary_key=True)
    driver_username: Union[str, Column] = Column(String)
    driver_latitude: Union[float, Column] = Column(Float)
    driver_longitude: Union[float, Column] = Column(Float)
    created_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    def from_entity(trip: Trip) -> TakenTripDTO:
        return TakenTripDTO(
            id=trip.id,
            driver_username=trip.state.driver_username(),
            driver_latitude=trip.state.driver_latitude(),
            driver_longitude=trip.state.driver_longitude())
