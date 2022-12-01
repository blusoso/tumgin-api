from sqlalchemy.orm import Session
from . import model, schema
from fastapi import HTTPException

DEFAULT_LIMIT_RECIPE_TAG = 100


def get_recipe_tags(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_RECIPE_TAG):
    return db.query(model.RecipeTag).offset(skip).limit(limit).all()


def create_recipe_tag(tag: schema.RecipeTagCreate, db: Session):
    db_recipe_tag = model.RecipeTag(**tag.dict())
    db.add(db_recipe_tag)
    db.commit()
    db.refresh(db_recipe_tag)
    return db_recipe_tag
