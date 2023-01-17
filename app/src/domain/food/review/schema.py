from pydantic import BaseModel
from datetime import datetime
from ...user.schema import User


class ReviewBase(BaseModel):
    recipe_id: int | None = None
    rating: int | None = None
    comment: str
    sub_comment_of: int | None = None

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    user_id: int

    class Config:
        orm_mode = True


class Review(ReviewBase):
    id: int
    user: User
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
