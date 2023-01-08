from pydantic import BaseModel
from datetime import datetime
from typing import List

class DietTypeBase(BaseModel):
    name: str
    emoji: str | None = None
    description: str | None = None
    foods_allowed: List[str] | None = None
    foods_restricted: List[str] | None = None


class DietTypeCreate(DietTypeBase):
    class Config:
        orm_mode = True


class DietType(DietTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True