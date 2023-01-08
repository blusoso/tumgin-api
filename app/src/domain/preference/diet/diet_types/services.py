from sqlalchemy.orm import Session
from . import model, schema

DEFAULT_LIMIT_DIET_TYPE = 100

def get_all_diet_types(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_DIET_TYPE):
    return db.query(model.DietType).offset(skip).limit(limit).all()

def create_diet_type(diet_type: schema.DietTypeCreate, db: Session):
    db_diet_type = model.DietType(**diet_type.dict())
    db.add(db_diet_type)
    db.commit()
    db.refresh(db_diet_type)
    return db_diet_type