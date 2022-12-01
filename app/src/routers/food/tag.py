from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.tags import schema, services

router = APIRouter(prefix='/tag', tags=["tag"])


@router.get('/', response_model=List[schema.Tag])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = services.get_tags(db, skip, limit)
    return tags


@router.post('/', response_model=schema.Tag)
def create_tag(tag: schema.TagCreate, db: Session = Depends(get_db)):
    new_tag = services.create_tag(tag, db)
    return new_tag
