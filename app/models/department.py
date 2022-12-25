from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.settings import settings


class DepartmentModel(settings.DBBaseModel):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    users = relationship("SellerModel", cascade="all,delete")
