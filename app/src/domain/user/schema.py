from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    password_hash: str

    class Config:
        orm_mode = True


class UserJWT(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class User(UserJWT):
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
