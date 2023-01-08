from pydantic import BaseModel
from datetime import datetime

from ....user.schema import User
from ....food.ingredients.schema import Ingredient


class UserAllergyBase(BaseModel):
    user_id: int
    ingredient_id: int


class  UserAllergyCreate(UserAllergyBase):
    class Config:
        orm_mode = True


class UserAllergy(BaseModel):
    id: int
    user: User
    ingredient: Ingredient
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True