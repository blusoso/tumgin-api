from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.user_like_recipe import schema, services

router = APIRouter(prefix='/like', tags=["user like recipe"])


@router.get('/{user_id}')
def get_like_recipes(user_id: int, db: Session = Depends(get_db)):
    like_recipes_list = services.get_like_recipes(db, user_id)
    return like_recipes_list


@router.get('/{user_id}/{recipe_id}', response_model=schema.UserLikeRecipe)
def get_recipe(user_id: int, recipe_id: int, db: Session = Depends(get_db)):
    recipe = services.get_user_like_recipe(db, user_id, recipe_id)
    return recipe


@router.put('/', response_model=schema.UserLikeRecipe)
def update_user_like_recipe(user_like_recipe: schema.UserLikeRecipeCreate, db: Session = Depends(get_db)):
    new_user_like_recipe = services.update_user_like_recipe(
        user_like_recipe, db)
    return new_user_like_recipe
