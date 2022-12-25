from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Marketing",
            }
        }


class DepartmentSchemaCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Eletronics",
            }
        }
