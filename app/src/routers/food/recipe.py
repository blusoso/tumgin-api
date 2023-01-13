from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.recipes import schema, services

router = APIRouter(prefix='/recipe', tags=["recipe"])


@router.get('/')
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = services.get_recipes(db, skip, limit)
    db_recipes = services.create_recipe_list_response(recipes)
    return db_recipes


@router.get('/{id}')
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = services.get_recipe(db, id)
    db_recipe = services.create_recipe_response(recipe)
    return db_recipe


@router.post('/', response_model=schema.RecipeCreate)
def create_recipe(recipe: schema.RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = services.create_recipes(recipe, db)
    return new_recipe
