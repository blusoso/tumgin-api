from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.recipe_ingredient import schema, services

router = APIRouter(prefix='/recipe-ingredient', tags=["recipe ingredient"])


@router.get('/', response_model=List[schema.RecipeIngredient])
def get_recipe_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipe_ingredients = services.get_recipe_ingredients(db, skip, limit)
    return recipe_ingredients


@router.get('/{recipe_id}', response_model=List[schema.RecipeIngredient])
def get_ingredient_from_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe_ingredients = services.get_ingredient_from_recipe(db, recipe_id)
    return recipe_ingredients


@router.post('/', response_model=schema.RecipeIngredient)
def create_recipe_ingredient(recipe: schema.RecipeIngredientCreate, db: Session = Depends(get_db)):
    new_recipe_ingredient = services.create_recipe_ingredient(recipe, db)
    return new_recipe_ingredient
