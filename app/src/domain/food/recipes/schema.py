from pydantic import BaseModel
from datetime import datetime

from ...user.schema import User


class RecipeBase(BaseModel):
    name: str
    name_en: str
    slug: str | None = None
    description: str | None = None
    thumbnail_img: str | None = None
    difficult_level: int
    calory: float | None = None
    minute: int | None = None
    serving: int | None = None
    protein_gram: float | None = None
    protein_percent: float | None = None
    fat_gram: float | None = None
    fat_percent: float | None = None
    carb_gram: float | None = None
    carb_percent: float | None = None
    is_staff_pick: bool

    class Config:
        orm_mode = True


class RecipeCreate(RecipeBase):
    user_id: int | None = None
    is_active: bool | None = True

    class Config:
        orm_mode = True


class Recipe(RecipeBase):
    id: int
    user: User
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True


class RecipeResponse(RecipeBase):
    username: str
    profile_img: str
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
