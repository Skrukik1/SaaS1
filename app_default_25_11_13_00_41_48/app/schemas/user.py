from pydantic import BaseModel, EmailStr, constr, validator
from typing import List, Optional


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)
    roles: Optional[List[str]] = []

    @validator("roles", pre=True, always=True)
    def default_roles(cls, v):
        return v or []


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[constr(min_length=6)]
    roles: Optional[List[str]]

    @validator("roles")
    def roles_non_empty(cls, v):
        if v is not None and not isinstance(v, list):
            raise ValueError("roles must be a list")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: List[str]

    class Config:
        orm_mode = True
