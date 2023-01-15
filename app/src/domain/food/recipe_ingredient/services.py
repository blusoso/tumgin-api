from sqlalchemy.orm import Session
from . import model, schema
from fastapi import HTTPException
from sqlalchemy import and_

DEFAULT_LIMIT_RECIPE_INGREDIENT = 100


def get_recipe_ingredients(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE_INGREDIENT):
    return db.query(model.RecipeIngredient)\
        .filter(model.RecipeIngredient.is_active == True)\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_ingredient_from_recipe(db: Session, recipe_id: int):
    return db.query(model.RecipeIngredient)\
        .filter(model.RecipeIngredient.recipe_id == recipe_id)\
        .all()


def check_exit_recipe_ingredient(recipe_id: int, ingredient_id: int, db: Session):
    return db.query(model.RecipeIngredient)\
        .filter(and_(
            model.RecipeIngredient.recipe_id == recipe_id,
            model.RecipeIngredient.ingredient_id == ingredient_id,
        )).first()


def check_recipe_ingredient_duplicate(recipe_id: int, ingredient_id: int, db: Session):
    exited_row = check_exit_recipe_ingredient(recipe_id, ingredient_id, db)

    if exited_row is not None:
        raise HTTPException(
            status_code=400, detail="Duplicate recipe ingredient")


def create_recipe_ingredient(recipe_ingredient: schema.RecipeIngredientCreate, db: Session):
    check_recipe_ingredient_duplicate(
        recipe_ingredient.recipe_id, recipe_ingredient.ingredient_id, db)

    db_recipe_ingredient = model.RecipeIngredient(**recipe_ingredient.dict())
    db.add(db_recipe_ingredient)
    db.commit()
    db.refresh(db_recipe_ingredient)
    return db_recipe_ingredient
