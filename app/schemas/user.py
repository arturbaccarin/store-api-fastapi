from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    disabled: Optional[bool]

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchema):
    password: str


class UserSchemaPassword(BaseModel):
    password: str
