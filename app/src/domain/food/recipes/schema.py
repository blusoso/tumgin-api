from pydantic import BaseModel
from typing import List


class RecipeBase(BaseModel):
    name: str
    minutes: int = 0
    serve: int = 1
    description: str | None = None
    steps: list[str] = []
    n_ingredients: int
    is_active: bool

    class Config:
        orm_mode = True


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True
