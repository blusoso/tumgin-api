from pydantic import BaseModel
from datetime import datetime


class IngredientBase(BaseModel):
    name: str
    name_en: str
    slug: str | None = None
    emoji: str | None = None
    description: str | None = None
    is_allergy: bool | None = False
    is_active: bool | None = True

    class Config:
        orm_mode = True


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
