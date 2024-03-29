from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.orm import subqueryload, eagerload, joinedload
import ast

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


def find_recipe_image_type(recipe_images, image_type: str):
    return [image for image in recipe_images if image.type == image_type]


def get_recipes(db: Session, user_id: int | None = None, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE):
    db_recipes = db.query(model.Recipe)\
        .options(joinedload('user'))\
        .options(joinedload('recipe_images').joinedload('image'))\
        .filter(model.Recipe.is_active == True)\
        .filter(model.Recipe.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()

    total_recipes = db.query(model.Recipe) \
        .filter(model.Recipe.is_active == True) \
        .filter(model.Recipe.deleted_at == None) \
        .count()

    if user_id is not None:
        for recipe in db_recipes:
            recipe.is_like = False
            recipe.is_like = create_is_like(db, recipe, user_id, recipe.id)

            recipe.thumbnail_img = find_recipe_image_type(
                recipe.recipe_images, 'thumbnail')
            if len(recipe.thumbnail_img) > 0:
                recipe.thumbnail_img = recipe.thumbnail_img[0].image.img
            else:
                recipe.thumbnail_img = None

    return {'total_recipes': total_recipes, 'recipes': db_recipes}


def get_recipe(db: Session, recipe_id: int, user_id: int | None = None):
    db_recipe = db.query(model.Recipe)\
        .options(subqueryload('recipe_images').joinedload('image'))\
        .options(subqueryload('user_like_recipes'))\
        .options(subqueryload('user'))\
        .options(subqueryload('recipe_ingredients').joinedload('ingredient'))\
        .options(subqueryload('directions'))\
        .options(subqueryload('reviews').joinedload('user'))\
        .filter(model.Recipe.id == recipe_id)\
        .filter(model.Recipe.is_active == True)\
        .filter(model.Recipe.deleted_at == None)\
        .first()

    db_recipe.is_like = False
    db_recipe.review_amount = 0
    db_recipe.review_avg = 0

    if user_id is not None:
        db_recipe.is_like = create_is_like(db, db_recipe, user_id, recipe_id)

    if len(db_recipe.reviews) > 0:
        db_recipe.review_amount = len(db_recipe.reviews)

        reviews_with_rating = [
            review for review in db_recipe.reviews if review.rating > 0]
        total_ratings = sum(review.rating for review in reviews_with_rating)
        average_rating = total_ratings / len(reviews_with_rating)
        db_recipe.review_avg = round(average_rating, 1)

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

    if recipe.protein_gram:
        recipe.protein_percent = calculate_nutrition_percentage(
            recipe.protein_gram, total_weight)

    if recipe.fat_gram:
        recipe.fat_percent = calculate_nutrition_percentage(
            recipe.fat_gram, total_weight)

    if recipe.carb_gram:
        recipe.carb_percent = calculate_nutrition_percentage(
            recipe.carb_gram, total_weight)

    db_recipe = model.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe
