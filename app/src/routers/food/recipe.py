from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.recipes import schema, services

router = APIRouter(prefix='/recipe', tags=["recipe"])


@router.get('/')
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = services.get_recipes(db, skip, limit)
    return recipes


@router.post('/', response_model=schema.RecipeCreate)
def create_recipe(recipe: schema.RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = services.create_recipes(recipe, db)
    return new_recipe
