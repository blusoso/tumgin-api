from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    is_active: bool

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True
