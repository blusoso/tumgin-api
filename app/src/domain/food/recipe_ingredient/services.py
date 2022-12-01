from sqlalchemy.orm import Session
from . import model, schema
from fastapi import HTTPException

DEFAULT_LIMIT_RECIPE_INGREDIENT = 100


def get_recipe_ingredients(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE_INGREDIENT):
    return db.query(model.RecipeIngredient).offset(skip).limit(limit).all()


def create_recipe_ingredient(recipe_ingredient: schema.RecipeIngredientCreate, db: Session):
    db_recipe_ingredient = model.RecipeIngredient(**recipe_ingredient.dict())
    db.add(db_recipe_ingredient)
    db.commit()
    db.refresh(db_recipe_ingredient)
    return db_recipe_ingredient
