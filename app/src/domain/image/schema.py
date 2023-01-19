from pydantic import BaseModel
from datetime import datetime


class ImageBase(BaseModel):
    img: str
    img_format: str | None = 'jpg'
    img_size: float | None = 0

    class Config:
        orm_mode = True


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True
