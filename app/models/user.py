from sqlalchemy import Integer, String, Column, Boolean

from core.settings import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    disabled = Column(Boolean, default=False)
