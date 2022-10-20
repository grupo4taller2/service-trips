from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URI: str
    API_V1_STR: str = os.environ.get("API_VERSION_PREFIX")
