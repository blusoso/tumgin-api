from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.orm import subqueryload

from ....util.text import create_slug

from . import model, schema
from ...user.model import User
from ...food.user_like_recipe.services import get_user_like_recipe

DEFAULT_LIMIT_RECIPE = 100


def create_is_like(db, db_recipe, user_id, recipe_id):
    db_user_like_recipe = get_user_like_recipe(db, user_id, recipe_id)

    if db_user_like_recipe is not None:
        if db_user_like_recipe.deleted_at:
            db_recipe.is_like = False
        else:
            db_recipe.is_like = True

    return db_recipe.is_like


def get_recipes(db: Session, user_id: int | None = None, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE):
    db_recipes = db.query(model.Recipe)\
        .options(subqueryload('user_like_recipes'))\
        .options(subqueryload('user'))\
        .filter(User.is_active == True)\
        .filter(model.Recipe.is_active == True)\
        .filter(model.Recipe.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()

    if user_id is not None:
        for recipe in db_recipes:
            recipe.is_like = False
            recipe.is_like = create_is_like(db, recipe, user_id, recipe.id)

    return db_recipes


def get_recipe(db: Session, recipe_id: int, user_id: int | None = None):
    db_recipe = db.query(model.Recipe)\
        .options(subqueryload('user_like_recipes'))\
        .options(subqueryload('user'))\
        .options(subqueryload('recipe_ingredients').joinedload('ingredient'))\
        .options(subqueryload('directions'))\
        .filter(model.Recipe.id == recipe_id)\
        .filter(model.Recipe.is_active == True)\
        .filter(model.Recipe.deleted_at == None)\
        .first()

    db_recipe.is_like = False

    if user_id is not None:
        db_recipe.is_like = create_is_like(db, db_recipe, user_id, recipe_id)

    db_recipe.directions = sorted(db_recipe.directions,
                                  key=lambda x: x.step_number,
                                  reverse=False)

    return db_recipe


def calculate_nutrition_percentage(item_weight: float, total_weight: float):
    result = 100 * item_weight / total_weight
    return Decimal(result).quantize(Decimal('0.0'))


def create_recipes(recipe: schema.RecipeCreate, db: Session):
    recipe.slug = create_slug(recipe.name_en)

    total_weight = recipe.protein_gram + recipe.fat_gram + recipe.carb_gram
    recipe.protein_percent = calculate_nutrition_percentage(
        recipe.protein_gram, total_weight)
    recipe.fat_percent = calculate_nutrition_percentage(
        recipe.fat_gram, total_weight)
    recipe.carb_percent = calculate_nutrition_percentage(
        recipe.carb_gram, total_weight)

    db_recipe = model.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe
