from pydantic import BaseModel
from datetime import datetime


class UserLikeRecipeBase(BaseModel):
    user_id: int
    recipe_id: int | None = None

    class Config:
        orm_mode = True


class UserLikeRecipeCreate(UserLikeRecipeBase):
    class Config:
        orm_mode = True


class UserLikeRecipe(UserLikeRecipeBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
