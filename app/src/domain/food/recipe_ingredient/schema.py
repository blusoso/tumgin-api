from pydantic import BaseModel
from ..recipes.schema import Recipe
from ..ingredients.schema import Ingredient


class RecipeIngredientBase(BaseModel):
    quantity: int
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
    recipe: Recipe
    ingredient: Ingredient

    class Config:
        orm_mode = True
