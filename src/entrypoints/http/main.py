from fastapi import FastAPI, APIRouter
from src.conf.config import Settings
from src.entrypoints.http.api.v1 import api


root_router = APIRouter()
app = FastAPI(title="Trips API", openapi_url="/openapi.json")

app.include_router(api.api_router, prefix=Settings().API_V1_STR)
app.include_router(root_router)
