from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.ingredients import schema, services

router = APIRouter(prefix='/ingredient', tags=["ingredient"])


@router.get('/', response_model=List[schema.Ingredient])
def get_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = services.get_ingredients(db, skip, limit)
    return tags


@router.post('/', response_model=schema.Ingredient)
def create_ingredient(ingredient: schema.IngredientCreate, db: Session = Depends(get_db)):
    new_ingredient = services.create_ingredient(ingredient, db)
    return new_ingredient
