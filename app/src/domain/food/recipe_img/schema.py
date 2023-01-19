from pydantic import BaseModel
from datetime import datetime

from ...image.schema import Image


class RecipeImageBase(BaseModel):
    recipe_id: int
    type: str

    class Config:
        orm_mode = True


class RecipeIngredientCreate(RecipeImageBase):
    image_id: int


class RecipeIngredient(RecipeImageBase):
    id: int
    image: Image
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
