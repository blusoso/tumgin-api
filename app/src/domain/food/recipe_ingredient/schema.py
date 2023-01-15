from pydantic import BaseModel
from ..recipes.schema import Recipe
from datetime import datetime

from ..ingredients.schema import Ingredient


class RecipeIngredientBase(BaseModel):
    quantity: float
    unit: str
    is_optional: bool = False
    is_active: bool

    class Config:
        orm_mode = True


class RecipeIngredientCreate(RecipeIngredientBase):
    recipe_id: int
    ingredient_id: int


class RecipeIngredient(RecipeIngredientBase):
    id: int
    recipe_id: int
    ingredient: Ingredient
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
