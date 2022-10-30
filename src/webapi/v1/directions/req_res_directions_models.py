from pydantic.main import BaseModel
from pydantic import Field


class DistanceResponse(BaseModel):
    meters: int = Field(example=3201)
    repr: str = Field(example='3.2 km')


class TimeResponse(BaseModel):
    seconds: int = Field(example=303)
    repr: str = Field(example='5 mins')


class DirectionsSearchRequest(BaseModel):
    origin: str = Field(example='Av. Paseo Colón 850, Buenos Aires')
    destination: str = Field(example='Gral. Las Heras 2214, Buenos Aires')


class DirectionsResponse(BaseModel):
    origin_address: str = Field(example='Av. Paseo Colón 850, Buenos Aires')
    origin_latitude: float = Field(example=-34.6174679)
    origin_longitude: float = Field(example=-58.36779029)
    destination_address: str = Field(
        example='Gral. Las Heras 2214, Buenos Aires'
    )
    destination_latitude: float = Field(example=-34.5885498)
    destination_longitude: float = Field(example=-58.3962364)
    estimated_time: TimeResponse
    distance: DistanceResponse

    class Config:
        arbitrary_types_allowed = True
