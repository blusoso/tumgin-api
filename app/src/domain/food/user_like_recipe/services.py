from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from ..recipes.model import Recipe
from ...user.model import User

from . import model, schema

DEFAULT_LIMIT_USER_LIKE_RECIPE = 100


def get_user_like_recipe(db: Session, user_id: int, recipe_id: int):
    return db.query(model.UserLikeRecipe)\
        .filter(model.UserLikeRecipe.user_id == user_id)\
        .filter(model.UserLikeRecipe.recipe_id == recipe_id)\
        .first()


def check_exit_user_like_recipe(user_like_recipe: schema.UserLikeRecipeCreate, db: Session):
    return db.query(model.UserLikeRecipe)\
        .filter(and_(
            model.UserLikeRecipe.user_id == user_like_recipe.user_id,
            model.UserLikeRecipe.recipe_id == user_like_recipe.recipe_id,
        )).first()


def check_user_like_recipe_duplicate(user_like_recipe: schema.UserLikeRecipeCreate, db: Session):
    exited_row = check_exit_user_like_recipe(user_like_recipe, db)

    return exited_row


def update_user_like_recipe(user_like_recipe: schema.UserLikeRecipeCreate, db: Session):
    exited_row = check_user_like_recipe_duplicate(user_like_recipe, db)

    if exited_row is not None:
        db_user_like_recipe = get_user_like_recipe(
            db, user_like_recipe.user_id, user_like_recipe.recipe_id)

        if db_user_like_recipe.deleted_at is None:
            db_user_like_recipe.deleted_at = datetime.utcnow()
        else:
            db_user_like_recipe.deleted_at = None

    else:
        db_user_like_recipe = model.UserLikeRecipe(
            **user_like_recipe.dict())
        db.add(db_user_like_recipe)

    db.commit()
    db.refresh(db_user_like_recipe)

    return db_user_like_recipe


def get_like_recipes(db: Session, user_id: int, skip: int = 0, limit: int = DEFAULT_LIMIT_USER_LIKE_RECIPE):
    db_like_recipes = db.query(model.UserLikeRecipe.id, Recipe, User)\
        .join(Recipe, Recipe.id == model.UserLikeRecipe.recipe_id)\
        .join(User, Recipe.user_id == User.id)\
        .filter(model.UserLikeRecipe.user_id == user_id)\
        .filter(model.UserLikeRecipe.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return db_like_recipes
