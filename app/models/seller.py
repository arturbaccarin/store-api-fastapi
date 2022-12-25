from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float

from core.settings import settings


class SellerModel(settings.DBBaseModel):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    base_salary = Column(Float)

    department_id = Column(Integer, ForeignKey("departments.id"))
