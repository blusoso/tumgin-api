from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from fastapi.param_functions import Path

from ...dependencies import get_db
from ...domain.food.recipes import schema, services

router = APIRouter(prefix='/recipe', tags=["recipe"])


@router.get('/')
def get_recipes(user_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = services.get_recipes(db, user_id, skip, limit)
    # db_recipes = services.create_recipe_list_response(recipes)
    return recipes


@router.get('/{recipe_id}')
def get_recipe(recipe_id: int, user_id: int | None = None, db: Session = Depends(get_db)):
    recipe = services.get_recipe(db, recipe_id, user_id)
    return recipe


@router.post('/', response_model=schema.RecipeCreate)
def create_recipe(recipe: schema.RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = services.create_recipes(recipe, db)
    return new_recipe
