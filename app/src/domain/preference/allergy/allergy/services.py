from sqlalchemy.orm import Session
from sqlalchemy import and_

from ....food.ingredients import model, schema

DEFAULT_LIMIT_ALLERGY = 100

def get_all_allergies(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_ALLERGY):
    return db.query(model.Ingredient)\
    .filter(and_(model.Ingredient.is_allergy == True, model.Ingredient.is_active == True))\
    .offset(skip)\
    .limit(limit)\
    .all()