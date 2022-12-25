from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://admin:root@localhost:5432/db"
    DBBaseModel = declarative_base()


settings = Settings()
