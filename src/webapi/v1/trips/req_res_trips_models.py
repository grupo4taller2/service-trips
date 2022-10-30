from pydantic.main import BaseModel
from pydantic import Field


class TripRequestRequest(BaseModel):
    rider_username: str = Field(example='mateoicalvo')
    rider_origin_address: str = Field(example='Av. Paseo Colón 850')
    rider_destination_address: str = Field(example='Gral. Las Heras 2214')
    trip_type: str = Field(example='regular')


class TripGetRequest(BaseModel):
    id: str = Field(example='30afdcdb-1580-4a4f-b9b3-c1381c28b05c')


class LocationResponse(BaseModel):
    address: str = Field(example='Av. Paseo Colón 850, Buenos Aires')
    latitude: float = Field(example=-34.6174679)
    longitude: float = Field(example=-58.367790)


class TripResponse(BaseModel):
    id: str = Field(example='9c8b9696-e802-49d8-8ff6-a6296ecb08f9')
    rider_username: str = Field(example='mateoicalvo')
    origin: LocationResponse
    destination: LocationResponse
    estimated_time: str = Field(example='17 mins')
    trip_type: str = Field(example='regular')
    distance: str = Field(example='1.1 km')
    state: str = Field(example='looking_for_driver')

    class Config:
        arbitrary_types_allowed = True
