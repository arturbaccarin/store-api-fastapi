from datetime import date
from pydantic import BaseModel, EmailStr


class SellerSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    birth_date: date
    base_salary: float
    department_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Carl Herman",
                "email": "carl.herman@example.com",
                "birth_date": "1984-05-07",
                "base_salary": 5000.0,
                "department_id": 2,
            }
        }


class SellerSchemaCreate(BaseModel):
    name: str
    email: EmailStr
    birth_date: date
    base_salary: float
    department_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Jenny Foster",
                "email": "jenny.foster@example.com",
                "birth_date": "1996-02-27",
                "base_salary": 4500.0,
                "department_id": 1,
            }
        }
