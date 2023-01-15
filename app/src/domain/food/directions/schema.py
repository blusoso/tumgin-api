from pydantic import BaseModel
from datetime import datetime


class DirectionBase(BaseModel):
    recipe_id: int
    step_number: int | None = None
    description: str
    is_active: bool | None = True

    class Config:
        orm_mode = True


class DirectionCreate(DirectionBase):
    pass


class Direction(DirectionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
