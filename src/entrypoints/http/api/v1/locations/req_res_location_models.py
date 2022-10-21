from pydantic.main import BaseModel
from pydantic import Field


class LocationSearchRequest(BaseModel):
    address: str = Field(example="Av. Paseo Colón 850")


class LocationResponse(LocationSearchRequest):
    latitude: float = Field(example=-33.01234)
    longitude: float = Field(example=-34.54321)
