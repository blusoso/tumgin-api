from pydantic import BaseModel
from datetime import datetime


class IngredientBase(BaseModel):
    name: str
    slug: str
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
    updated_at: datetime
    deleted_at: datetime

    class Config:
        orm_mode = True
