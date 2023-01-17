from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...dependencies import get_db
from ...domain.food.review import schema, services

router = APIRouter(prefix='/review', tags=["review"])


@router.get('/{recipe_id}', response_model=List[schema.Review])
def get_reviews(recipe_id: int, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    reviews = services.get_reviews(db, recipe_id, skip, limit)
    return reviews


@router.post('/', response_model=schema.Review)
def create_review(review: schema.ReviewCreate, db: Session = Depends(get_db)):
    new_review = services.create_review(review, db)
    return new_review
