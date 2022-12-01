from pydantic import BaseModel
from ..recipes.schema import Recipe
from ..tags.schema import Tag


class RecipeTagBase(BaseModel):
    is_active: bool

    class Config:
        orm_mode = True


class RecipeTagCreate(RecipeTagBase):
    recipe_id: int
    tag_id: int

    class Config:
        orm_mode = True


class RecipeTag(RecipeTagBase):
    id: int
    recipe: Recipe
    tag: Tag

    class Config:
        orm_mode = True
