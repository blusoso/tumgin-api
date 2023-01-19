from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..domain.image import schema, services

router = APIRouter(prefix='/image', tags=["image"])


@router.get('/', response_model=List[schema.Image])
def get_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_created = services.get_images(db, skip, limit)
    return user_created


@router.post('/', response_model=schema.Image)
def create_image(image: schema.ImageCreate, db: Session = Depends(get_db)):
    new_image = services.create_image(image, db)
    return new_image
