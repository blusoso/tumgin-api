from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    gender: int
    profile_img: str | None = None
    role: str | None = "user"


class UserCreate(UserBase):
    password: constr(min_length=8)
    login_with: str | None = 'site'
    is_consent: bool = True

    class Config:
        orm_mode = True


class UserJWT(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class User(UserJWT):
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: constr(min_length=8)

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True

class RefreshToken(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True