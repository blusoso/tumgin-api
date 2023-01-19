from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.food.recipe_img import schema, services

router = APIRouter(prefix='/recipe_img', tags=["recipe image"])


@router.post('/')
def create_recipe_image(recipe_image: schema.RecipeIngredientCreate, db: Session = Depends(get_db)):
    recipe_image = services.create_recipe_image(recipe_image, db)
    return recipe_image


@router.get('/{recipe_id}')
def get_recipe_image(recipe_id: int, is_thumbnail: bool = False, db: Session = Depends(get_db)):
    if is_thumbnail:
        recipe_image = services.get_thumbnail(db, recipe_id)
    else:
        recipe_image = services.get_all_recipe_image(db, recipe_id)

    return recipe_image
