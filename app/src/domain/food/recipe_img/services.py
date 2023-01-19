from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_

from . import model, schema
from ...image.model import Image

DEFAULT_LIMIT_RECIPE_INGREDIENT = 100


def create_recipe_image(recipe_image: schema.RecipeIngredientCreate, db: Session):
    db_recipe_image = model.RecipeImage(**recipe_image.dict())
    db.add(db_recipe_image)
    db.commit()
    db.refresh(db_recipe_image)
    return db_recipe_image


def get_all_recipe_image(db: Session, recipe_id: int):
    return db.query(
        model.RecipeImage.recipe_id,
        model.RecipeImage.type,
        Image.img)\
        .join(Image, Image.id == model.RecipeImage.image_id)\
        .filter(model.RecipeImage.recipe_id == recipe_id)\
        .all()


def get_thumbnail(db: Session, recipe_id: int):
    return db.query(
        model.RecipeImage.recipe_id,
        model.RecipeImage.type,
        Image.img)\
        .join(Image, Image.id == model.RecipeImage.image_id)\
        .filter(model.RecipeImage.recipe_id == recipe_id)\
        .filter(model.RecipeImage.type == 'thumbnail')\
        .first()
