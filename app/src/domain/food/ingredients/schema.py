from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    emoji: str | None = None
    is_allergy: bool | None = False
    is_active: bool| None = True

    class Config:
        orm_mode = True


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True
