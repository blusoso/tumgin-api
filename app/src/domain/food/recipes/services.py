from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import model, schema
from ..recipe_ingredient.model import RecipeIngredient
from ..ingredients.model import Ingredient

DEFAULT_LIMIT_RECIPE = 100


def get_recipes(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE):
    db_recipe = db.query(
        model.Recipe.name,
        model.Recipe.description,
        model.Recipe.n_ingredients,
        model.Recipe.serve,
        model.Recipe.steps,
        Ingredient.emoji,
        Ingredient.name.label('ingredient_name'),
        RecipeIngredient.quantity,
        RecipeIngredient.unit,
        RecipeIngredient.is_optional,
    )\
        .join(RecipeIngredient, RecipeIngredient.recipe_id == model.Recipe.id)\
        .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)\
        .filter(model.Recipe.is_active == True)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return db_recipe


def create_recipes(recipe: schema.RecipeCreate, db: Session):
    db_recipe = model.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
