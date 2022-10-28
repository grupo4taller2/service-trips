from pydantic.main import BaseModel
from pydantic import Field


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
    estimated_time: str = Field(example='33 mins')
    distance: str = Field(example='6.8 km')
