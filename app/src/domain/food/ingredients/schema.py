from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    emoji: str | None = None
    is_active: bool

    class Config:
        orm_mode = True


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True
