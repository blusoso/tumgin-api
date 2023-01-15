from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.directions import schema, services

router = APIRouter(prefix='/direction', tags=["direction"])


@router.get('/')
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = services.get_recipes(db, skip, limit)
    db_recipes = services.create_recipe_list_response(recipes)
    return db_recipes


@router.get('/{id}')
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = services.get_recipe(db, id)
    # db_recipe = services.create_recipe_response(recipe)
    return recipe


@router.post('/')
def create_direction(direction: schema.DirectionCreate, db: Session = Depends(get_db)):
    new_direction = services.create_direction(direction, db)
    return new_direction
