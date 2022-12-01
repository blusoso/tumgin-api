from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.recipe_tag import schema, services

router = APIRouter(prefix='/recipe-tag', tags=["recipe tag"])


@router.get('/', response_model=List[schema.RecipeTag])
def get_recipe_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipe_tags = services.get_recipe_tags(db, skip, limit)
    return recipe_tags


@router.post('/', response_model=schema.RecipeTag)
def create_recipe_tag(recipe: schema.RecipeTagCreate, db: Session = Depends(get_db)):
    new_recipe_tag = services.create_recipe_tag(recipe, db)
    return new_recipe_tag
