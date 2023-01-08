from pydantic import BaseModel
from datetime import datetime

from ....user.schema import User
from ..diet_types.schema import DietType

class UserDietTypeBase(BaseModel):
    user_id: int
    diet_type_id: int

class UserDietTypeCreate(UserDietTypeBase):
    class Config:
        orm_mode = True


class UserDietType(BaseModel):
    id: int
    user: User
    diet_type: DietType
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True