from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.orm import subqueryload

from ....util.text import create_slug

from . import model, schema
from ...user.model import User
from ...food.user_like_recipe.model import UserLikeRecipe
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


def recipe_response(user, recipe):
    return schema.RecipeResponse(
        username=user.username,
        profile_img=user.profile_img,
        id=recipe.id,
        name=recipe.name,
        name_en=recipe.name_en,
        slug=recipe.slug,
        description=recipe.description,
        thumbnail_img=recipe.thumbnail_img,
        difficult_level=recipe.difficult_level,
        calory=recipe.calory,
        minute=recipe.minute,
        serving=recipe.serving,
        protein_gram=recipe.protein_gram,
        protein_percent=recipe.protein_percent,
        fat_gram=recipe.fat_gram,
        fat_percent=recipe.fat_percent,
        carb_gram=recipe.carb_gram,
        carb_percent=recipe.carb_percent,
        is_staff_pick=recipe.is_staff_pick,
        created_at=recipe.created_at
    )


def create_recipe_list_response(db_recipes):
    return [recipe_response(user, recipe) for user, recipe in db_recipes]


def create_recipe_response(db_recipe):
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    user, recipe = db_recipe
    return recipe_response(user, recipe)


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
