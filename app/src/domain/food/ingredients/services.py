from sqlalchemy.orm import Session
from . import model, schema
from fastapi import HTTPException

DEFAULT_LIMIT_INGREDIENT = 100


def get_ingredients(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_INGREDIENT):
    return db.query(model.Tag).offset(skip).limit(limit).all()


def create_ingredient(ingredient: schema.IngredientCreate, db: Session):
    db_ingredient = model.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient
