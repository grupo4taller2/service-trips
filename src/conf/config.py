from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URI: str = os.environ.get("DATABASE_URI")
    API_V1_STR: str = os.environ.get("API_VERSION_PREFIX")
    APP_ENV: os.environ.get("APP_ENV")
    TEST_ENV: str = 'testing'
