from sqlalchemy.orm import Session
from . import model, schema
from sqlalchemy import and_
from fastapi import HTTPException

DEFAULT_LIMIT_INGREDIENT = 100


def get_ingredients(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_INGREDIENT):
    return db.query(model.Ingredient).offset(skip).limit(limit).all()

def check_exit_ingredient(ingredient: schema.IngredientCreate, db: Session):
    return db.query(model.Ingredient)\
        .filter(and_(
            model.Ingredient.name == ingredient.name,
        )).first()

def check_ingredient_duplicate(ingredient: schema.IngredientCreate, db: Session):
    exited_row = check_exit_ingredient(ingredient, db)

    if exited_row is not None:
        raise HTTPException(status_code=400, detail="Duplicate ingredient")

def create_ingredient(ingredient: schema.IngredientCreate, db: Session):
    check_ingredient_duplicate(ingredient, db)

    db_ingredient = model.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient
